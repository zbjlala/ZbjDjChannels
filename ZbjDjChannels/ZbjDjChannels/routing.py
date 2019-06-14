from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chatroom.routing
import chatsolo.routing
import djim.routing
'''
此根路由配置指定在与Channels开发服务器建立连接时，
ProtocolTypeRouter将首先检查连接类型。如果它是WebSocket连接（ws：//或wss：//），
则将连接到AuthMiddlewareStack.
在AuthMiddlewareStack将填充的连接的范围与到当前认证的用户，
类似于Django的如何一个参考 AuthenticationMiddleware填充请求与当前认证的用户的图功能的对象。
（范围将在本教程的后面部分讨论。）然后将连接到URLRouter。
在URLRouter将检查连接到路由到一个特定的消费者，基于所提供的HTTP路径url模式。
'''
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
           chatroom.routing.websocket_urlpatterns + chatsolo.routing.websocket_urlpatterns + djim.routing.websocket_urlpatterns
            #chatroom.routing.websocket_urlpatterns,
            #chatsolo.routing.websocket_urlpatterns,

        )
    ),
})