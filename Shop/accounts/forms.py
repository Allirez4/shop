from django import forms
from django.contrib.auth.views import PasswordResetView
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
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



class LoginForm(forms.Form):
    username = forms.CharField(
        label='Email or Phone Number',
        widget=forms.TextInput(attrs={'placeholder': 'Enter email or phone'})
    )
    password = forms.CharField(widget=forms.PasswordInput())
    
User = get_user_model()
class hybridresetform(PasswordResetForm):
    email=forms.CharField(
        label='Email or Phone Number',
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder':'Enter email or phone'}))
    def get_users(self, email):
        if '@' in email:
            active_users = User.objects.filter(email__iexact=email, is_active=True)
        else:
            active_users = User.objects.filter(phone_number__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())
    
    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        
        email_or_phone = self.cleaned_data["email"]
        if '@' in email_or_phone:
            user=User.objects.filter(email__iexact=email_or_phone)
        else:
            user=User.objects.filter(phone_number__iexact=email_or_phone)
        if not user.exists():
            raise ValidationError("This account doesn't have an email address for password reset.")
        
        # Use the user's email for sending, regardless of how they searched
        self.cleaned_data["email"] = user.email
        return super().save(
            domain_override=domain_override,
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            use_https=use_https,
            token_generator=token_generator,
            from_email=from_email,
            request=request,
            html_email_template_name=html_email_template_name,
            extra_email_context=extra_email_context
        )