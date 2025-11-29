from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('list/', views.sessions, name='sessions'),
    path('chat/<str:session_id>/', views.room, name='room'),
]
