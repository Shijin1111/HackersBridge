from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/video/(?P<team_id>\d+)/$', consumers.ChatConsumer.as_asgi()),  # Update path here
]
