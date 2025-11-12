from django.urls import path
from . import api_views
app_name='accounts_api'
urlpatterns = [
    path('login/', api_views.login_api.as_view(), name='login_api'),
]