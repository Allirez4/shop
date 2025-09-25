from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
class UserManager(BaseUserManager):
    
    def Create_User(self,phone_number,email,full_name,password):
        if not phone_number :
            raise ValueError('user must have phone number')
        if not email:
            raise ValueError('user must have a email')
        if not full_name:
            raise ValueError('user must have a username')
        user=self.model(email=self.normalize_email(email),full_name=full_name,phone_number=phone_number,password=password)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,phone_number,email,full_name,password):
        user=self.Create_User(phone_number,email,full_name,password)
        user.is_admin=True
        user.save()
        return user