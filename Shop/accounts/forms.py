from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
class UserCreation(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)
    
    class Meta:  
        model = CustomUser
        fields = ['phone_number', 'email', 'full_name']  # Fixed typo in field name
    
    def clean_password2(self):  # Lowercase method name with underscore
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password mismatch')
        return cd['password2']  # Must return this
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user  # Missing return statement
class UserChange(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text="you cant change your password form<a ref=\"../password/\" this form </a>")
    class meta:
        model=CustomUser
        fields=['phone_number','email','full_name','last_login']
                
class UserRegistrationForm(forms.Form):
    full_name=forms.CharField(max_length= 30,label='FUll name')
    phone_number=forms.CharField(max_length=11,label="phone number")
    email=forms.EmailField()
    password=forms.CharField(max_length=50,widget=forms.PasswordInput)
class VerifyOtp(forms.Form):
    code=forms.IntegerField(max_value=99999)
