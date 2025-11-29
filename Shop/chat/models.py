from django.db import models
from accounts.models import CustomUser

class supportsession(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #session_id=models.IntegerField(blank=True, null=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    # def save(self, *args, **kwargs):
    #     if not self.session_id:
    #         self.session_id = self.user.id
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Support Session {self.user.id} for {self.user.username}"

class chatmessage(models.Model):
    sender=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_messages')
    session=models.ForeignKey(supportsession, on_delete=models.CASCADE)
    message=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"