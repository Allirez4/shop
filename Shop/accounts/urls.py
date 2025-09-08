from django.urls import path
from . import views
app_name='accounts'
urlpatterns = [
    path('registeration/',views.UserRgisterationView.as_view(),name='register'),
    path('verify/',views.OTPVerify.as_view(),name='verify'),
]