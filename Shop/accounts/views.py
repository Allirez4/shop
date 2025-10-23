from django.shortcuts import render,redirect
from django.views import View
from . import forms
from django.contrib import messages
from utils import sendOTP
from .models import otp
from django.contrib.auth.hashers import make_password
import random
from django.conf import settings
from .models import CustomUser 
from django.contrib.auth import authenticate, login ,logout, views as vv
from django.contrib import messages
from django.urls import reverse_lazy
from .tasks import send_password_reset_email_task
from django.template import loader
class UserRgisterationView(View):
    form=forms.UserRegistrationForm
    def get(self,request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already signed in.')
            return redirect('/')  
        return render(request,'accounts/register.html',{'form':self.form})
    def post(self,request):
        form=self.form(request.POST)
        if form.is_valid():
            try:
                OTP_code=random.randint(10000,99999)
                #form.save()
                num:str=form.cleaned_data['phone_number']
                num=num.replace('0','+98',1)
                sendOTP(num,OTP_code)
                otp.objects.update_or_create(phone_number=form.cleaned_data['phone_number'],defaults={'code':OTP_code})
                request.session['user_registeration_info']={
                    'phone_number':form.cleaned_data['phone_number'],
                    'email':form.cleaned_data['email'],
                    'full_name':form.cleaned_data['full_name'],
                    'password':form.cleaned_data['password'],
                }
                messages.success(request,"a code was was sent for you")
                
                return redirect('accounts:verify')
            except Exception as e:
                messages.error(request,f"try again {e}")
                return render(request,'accounts/register.html',{'form':self.form})
class OTPVerify(View):
    form=forms.VerifyOtp
    def get(self,request):
        print(99*'=')
        print(request.session['user_registeration_info'])
        return render(request,'accounts/verify.html',{'form':self.form})
    def post(self,request):
        form=self.form(request.POST)
        user_session=request.session['user_registeration_info']
        if form.is_valid():
            cd=form.cleaned_data
            otp_inestance=otp.objects.get(phone_number=user_session['phone_number'])
            if cd['code']==otp_inestance.code:
                messages.success(request,'registeration was successful')
                user=CustomUser.objects.Create_User(user_session['phone_number'],user_session['email'],user_session['full_name'],user_session['password'])
                otp_inestance.delete()
                #user=CustomUser.objects.get(phone_number=user_session['phone_number'])
                login(request,user=user,backend='accounts.backends.EmailPhoneAuthBackend')##########
                return redirect('/')
            else:
                messages.error(request,'your code is wrong')
                
                return redirect('accounts:verify')
class LoginView(View):
    form=forms.LoginForm
    def get(self,request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('/')  
        return render(request,'accounts/login.html',{'form':self.form})
    def post(self,request):
        form=self.form(request.POST)
        remember_me=request.POST.get('remember_me')
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd['username'],password=cd['password'])
            
            if user is not None:
                login(request,user)
                if remember_me:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                else:
                    request.session.set_expiry(0)
                messages.success(request,'you are logged in')
                return redirect('/')
            else:
                messages.error(request,'username or password is wrong')
                return render(request,'accounts/login.html',{'form':self.form})
        else:
            messages.error(request,'please correct the error below.')
            return render(request,'accounts/login.html',{'form':self.form})
class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,'you are logged out')
        return redirect('/')
class PasswordResetView(vv.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'registration/password_reset_email.txt'
    subject_template_name = 'registration/password_reset_subject.txt'
    form_class = forms.hybridresetform
    
    def form_valid(self, form):
        """Override form_valid to handle email sending via Celery"""
        email_or_phone = form.cleaned_data["email"]
        
        try:
            # Get the user (same logic as in your form)
            if '@' in email_or_phone:
                user = CustomUser.objects.get(email=email_or_phone, is_active=True)
            else:
                user = CustomUser.objects.get(phone_number=email_or_phone, is_active=True)
            
            if not user.email:
                # Still redirect to success page for security
                return redirect(self.success_url)
            
            # Build context for email template
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            
            context = {
                'email': user.email,
                'domain': self.request.get_host(),
                'site_name': 'Shop',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if self.request.is_secure() else 'http',
            }
            
            # Render email content
            subject = loader.render_to_string(self.subject_template_name, context)
            subject = ''.join(subject.splitlines())  # Remove newlines
            message = loader.render_to_string(self.email_template_name, context)
            
            # Send email asynchronously via Celery
            send_password_reset_email_task.delay(
                subject=subject,
                message=message,
                from_email=None,  # Use default from settings
                recipient_list=[user.email],
                html_message=None
            )
            
        except CustomUser.DoesNotExist:
            # Still redirect to success page for security (don't reveal if user exists)
            pass
        except Exception as e:
            # Still redirect to success page for security
            pass
        
        # Always redirect to success page
        return redirect(self.success_url)
class PasswordResetDoneView(vv.PasswordResetDoneView):
    template_name = 'accounts/done.html'

class PasswordResetConfirmView(vv.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class PasswordResetCompleteView(vv.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'