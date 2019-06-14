from django.conf.urls import url

from djim import consumers

websocket_urlpatterns = [
    url(r'^ws/djim/(?P<group_name>[^/]+)/$', consumers.ChatConsumer),
]