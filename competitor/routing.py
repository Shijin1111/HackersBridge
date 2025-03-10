from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/video/(?P<team_id>\d+)/$', consumers.ChatConsumer.as_asgi()),  # Update path here
    re_path(r"ws/hackathon_chat/$", consumers.HackathonChatConsumer.as_asgi()),
]
