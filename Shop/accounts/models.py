from django.db import models
from django.contrib.auth.models import AbstractUser
from . import managers
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number=models.CharField(max_length=11,unique=True)
    full_name=models.CharField(max_length=60)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    username=models.CharField(blank=True, null=True, max_length=50)
    city=models.CharField(max_length=50,blank=True,null=True)
    address=models.CharField(max_length=200,blank=True,null=True)
    postal_code=models.CharField(max_length=20,blank=True,null=True)
    national_code=models.CharField(max_length=10,blank=True,null=True,unique=True)
    
    USERNAME_FIELD='phone_number'
    REQUIRED_FIELDS=['email','full_name']
    objects= managers.UserManager()
    def __str__(self):
        return self.email
    def has_perm(self, perm_list, obj = None):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin
class otp(models.Model):
    phone_number=models.CharField(max_length=11)
    created_at=models.DateTimeField(auto_now=True)
    code=models.SmallIntegerField()    
    def __str__(self):
        return f'{self.phone_number} - {self.code} created at {self.created_at}'