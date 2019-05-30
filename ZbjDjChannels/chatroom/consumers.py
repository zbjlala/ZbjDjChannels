from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        '''
        self.scope [ 'url_route'] [ 'kwargs'] [ 'ROOM_NAME']
'room_name'从URL路由中获取参数chat/routing.py ，打开与消费者的WebSocket连接。
每个使用者都有一个范围，其中包含有关其连接的信息，特别是包括URL路由中的任何位置或关键字参数以及当前经过身份验证的用户（如果有）。
直接从用户指定的房间名称构造Channels组名称，不进行任何引用或转义。
组名只能包含字母，数字，连字符和句点。因此，此示例代码将在具有其他字符的房间名称上失败。

 async_to_sync（self.channel_layer.group_add）（...）
        加入一个小组。
        async_to_sync（...）包装器是必需的，因为ChatConsumer是一个同步WebsocketConsumer，但它调用异步通道层方法。（所有通道层方法都是异步的。）
        组名仅限于ASCII字母数字，连字符和句点。由于此代码直接从房间名称构造组名称，因此如果房间名称包含在组名称中无效的任何字符，则该名称将失败。
        self.accept（）
接受WebSocket连接。
如果不在connect（）方法中调用accept（），则拒绝并关闭连接。例如，您可能希望拒绝连接，因为请求的用户无权执行请求的操作。
如果您选择接受连接，建议将accept（）作为connect（）中的最后一个操作调用。
        '''
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, code):
        '''
        async_to_sync(self.channel_layer.group_discard)(…)
        Leaves a group.
        '''

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        '''
        async_to_sync（self.channel_layer.group_send）
        将事件发送给组。
        事件具有'type'与应该在接收事件的使用者上调用的方法名称相对应的特殊键。
        '''
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))



