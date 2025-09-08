from django.shortcuts import render,redirect
from django.views import View
from . import forms
from django.contrib import messages
from utils import sendOTP
from .models import otp
from django.contrib.auth.hashers import make_password
import random
from .models import CustomUser 

class UserRgisterationView(View):
    form=forms.UserRegistrationForm
    def get(self,request):
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
                otp.objects.create(phone_number=form.cleaned_data['phone_number'],code=OTP_code)
                request.session['user_registeration_info']={
                    'phone_number':form.cleaned_data['phone_number'],
                    'email':form.cleaned_data['email'],
                    'full_name':form.cleaned_data['full_name'],
                    'password':make_password(form.cleaned_data['password']),
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
                CustomUser.objects.Create_User(user_session['phone_number'],user_session['email'],user_session['full_name'],user_session['password'])
                otp_inestance.delete()
                return redirect('/')
            else:
                messages.error(request,'your code is wrong')
                return redirect('accounts:verify')
            