
from django.conf.urls import url

from chatroom import consumers

websocket_urlpatterns = [
    url(r'^ws/chatroom/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]