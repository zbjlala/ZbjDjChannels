import json
import threading
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer

from chatsolo.models import UserList
from chatsolo.serializers import user_list_json

class ChatConsumer(AsyncJsonWebsocketConsumer):
    chats = dict()
    lock = threading.Lock()


    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print('%s and %s' % (self.group_name, self.channel_name))
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        #将用户添加至聊天组信息chats中
        try:
            ChatConsumer.chats[self.group_name] = self.channel_name
        except:
            pass



        print(ChatConsumer.chats)
        #创建连接时调用
        await self.accept()




    async def disconnect(self, close_code):

        # 连接关闭时调用
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        # 将该客户端移除聊天组连接信息
        ChatConsumer.chats[self.group_name].remove(self)
        await self.close()

    '''当有两个用户连接这个聊天组时，我们就直接向这个聊天组发送信息。
    当只有一个用户连接这个聊天组时，我们就通过push/xxx/把信息发给接收方。
    '''
    async def receive_json(self, message, **kwargs):
        '''
        # 收到消息时调用
        to_user = message.get('to_user')
        print(to_user)
        # 信息发送
        length = len(ChatConsumer.chats[self.group_name])
        if length == 2:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": message.get('message'),
                },
            )
        else:
            await self.channel_layer.group_send(
                to_user,
                {
                    "type": "push.message",
                    "event": {'message': message.get('message'), 'group': self.group_name}
                }
            )
          '''
        if message.get('type') == 'userlist':
            lists = []
            print(ChatConsumer.chats)
            for (key, value) in ChatConsumer.chats.items():
                print(str(value)+': 1')
                listitem = UserList
                listitem.uid = key
                listitem.session = value
                l = json.dumps(listitem, default=user_list_json)
                print(l)
                lists.append(l)

            print(json.dumps(lists))
            # for i in lists:
                # print(json.dumps(str(i,encoding='utf-8')))
                # print(json.dumps(i,default=self.obj_userlist_json()))
                # print(str(i)+': 2')
            # print(str(list)+': 3')
            # print(json.dumps(lists, default=self.obj_userlist_json))
            await self.send_json({
                'type': 'userlist',
                'message': lists

               # "message": json.loads(lists)
              #  'message': [
        #{'uid': list(ChatConsumer.chats)[0], 'sid': list(ChatConsumer.chats.values())[0]}
            })

        if message.get('type') == 'solo':
            content = message.get('message')
            channelname = message.get('accepter')
            await self.channel_layer.send(channelname, {
                "type": 'chat.message',
                "message": content,
            })
            await self.send_json({
                'type': 'chat.message',
                'message': content
            })



    async def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        await self.send_json({
            "message": event["message"],
        })

    def obj_userlist_json(object):
        return{
            "uid": object.uid,
            "session": object.session
        }

# 推送consumer
class PushConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['username']

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def push_message(self, event):
        print(event)
        await self.send(text_data=json.dumps({
            "event": event['event']
        }))


