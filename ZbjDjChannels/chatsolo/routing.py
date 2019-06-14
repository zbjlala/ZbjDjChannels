from django.conf.urls import url

from chatsolo import consumers

'''
ws/chat/xxx/（xxx指代聊天组）这条路径是当聊天双方都进入同一个聊天组以后，开始聊天的路径。
push/xxx/（xxx指代用户名）这条是指当有一方不在聊天组，另一方的消息将通过这条路径推送给对方。
ws/chat/xxx/只有双方都进入聊天组以后才开启，而push/xxx/是自用户登录以后，直至退出都开启的。
'''
websocket_urlpatterns = [
    url(r'^ws/chatsolo/(?P<group_name>[^/]+)/$', consumers.ChatConsumer),
    url(r'^push/(?P<username>[0-9a-z]+)/$', consumers.PushConsumer),
]