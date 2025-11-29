import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import supportsession, chatmessage

class support_chat(AsyncWebsocketConsumer):
    
    async def connect(self):
        user = self.scope['user']
        
        if user.is_anonymous:
            await self.close()
            return
        
        # Get user_id from URL (always present now)
        user_id = self.scope['url_route']['kwargs']['user_id']
        self.session_id = user_id
        if user.is_staff:
            await self.channel_layer.group_add(
            f"support_{user_id}",
            self.channel_name
            )
            await self.accept()
        if user.is_authenticated and not user.is_staff:
            
            await self.channel_layer.group_add(
            f"support_{user.id}",
            self.channel_name
            )
            await self.accept()
        
        # Create session if user is not staff
        if not user.is_staff:
            await self.get_or_create_session(user)
    
    async def disconnect(self, close_code):
        if hasattr(self, 'session_id'):
            await self.channel_layer.group_discard(
                f"support_{self.session_id}",
                self.channel_name
            )
    
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')
            
            if not message.strip():
                return
            
            user = self.scope['user']
            
            if user.is_staff:
                # Staff member sending to a user's session
                session_id = self.scope['url_route']['kwargs']['user_id']
                session = await self.get_session_by_user_id(session_id)
            else:
                # Regular user sending to their own session
                session = await self.get_session_by_user(user)
                session_id = user.id  # ✅ Use user.id directly, not session.user.id
            
            # Save message to database
            await self.save_message(user, session, message)
            
            # Broadcast to group
            await self.channel_layer.group_send(
                f"support_{session_id}",
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': user.username or user.email,  # ✅ Handle case where username might be None
                    'sender_id': user.id,
                    'is_staff': user.is_staff,
                }
            )
            
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': f'Error: {str(e)}'
            }))
    
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],
            'is_staff': event['is_staff'],
        }))
    
    # ✅ Async database helper methods
    @database_sync_to_async
    def get_or_create_session(self, user):
        """Get or create support session for user"""
        session, created = supportsession.objects.get_or_create(
            user=user,
            defaults={'is_active': True}
        )
        return session
    
    @database_sync_to_async
    def get_session_by_user_id(self, user_id):
        """Get session by user ID (for admin)"""
        return supportsession.objects.get(user__id=user_id)
    
    @database_sync_to_async
    def get_session_by_user(self, user):
        """Get session by user object"""
        return supportsession.objects.get(user=user)
    
    @database_sync_to_async
    def save_message(self, sender, session, message):
        """Save chat message to database"""
        return chatmessage.objects.create(
            sender=sender,
            session=session,
            message=message
        )