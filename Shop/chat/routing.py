from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user_id>\w+)/$', consumers.support_chat.as_asgi()),
    re_path(r'ws/support/(?P<user_id>\w+)/$', consumers.support_chat.as_asgi()),
]