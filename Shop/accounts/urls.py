from django.urls import path
from . import views
app_name='accounts'
urlpatterns = [
    path('registeration/',views.UserRgisterationView.as_view(),name='register'),
    path('verify/',views.OTPVerify.as_view(),name='verify'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('password_reset/',views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/',views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_complete/',views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]