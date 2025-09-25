# accounts/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailPhoneAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            if hasattr(request, 'path') and '/admin/' in request.path:
                
                user = User.objects.get(
                    phone_number=username,
                    is_admin=True
                )
                
            # Look up user by either email or phone number
            elif '@'in username:
                    user = User.objects.get(email=username)
            elif username.isdigit() and len(username) == 11:
                user=User.objects.get(phone_number=username)
            else:        
                user = User.objects.get(
                Q(email=username) | Q(phone_number=username)
                )
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None