import datetime
import json
import socket

import redis as redis
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from djim.models import UserSession, channel, UserList
from djim.serializers import usersession_json, user_list_json
from utils import const, ipHelper


class ChatConsumer(AsyncJsonWebsocketConsumer):

    USER_SEEION = 'UserSession'
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r = redis.Redis(connection_pool=pool)


    #建立连接
    async def connect(self):
        self.group_name = 'common'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        #将user信息加入到reids
        try:
            print('222')
            userid = self.scope['url_route']['kwargs']['group_name']
            usersession = UserSession()
            print('333')
            usersession.name = userid
            print(userid)
            usersession.channel_name = self.channel_name
            print(self.channel_name)
            usersession.subIP = '127.0.0.1'
            #print(self.getLocalIP())
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            UserSession.activeTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(json.dumps(usersession, default=usersession_json))
            self.r.hset(self.USER_SEEION, self.channel_name, json.dumps(usersession, default=usersession_json))
            await self.accept()
        except Exception as e:
            print(e)
            # 创建连接时调用
            #await self.accept()

    #连接断开
    async def disconnect(self, close_code):

        # 连接关闭时调用
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        # 从Redis UserSession中删除当前用户
        try:
            self.r.hdel(self.USER_SEEION, self.channel_name)

        except:
            pass
        await self.close()

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        print(bytes_data)
        print(channel.user_list)
        if(text_data != None and bytes_data == None):
            json_text_data = json.loads(text_data)
            print(text_data)
            #群发消息
            if json_text_data['type'] == str(channel.chat_all):
                print(self.group_name)
                content = json_text_data['message']
                await self.channel_layer.group_send(
                    self.group_name, {
                        'sender': json_text_data['sender'],
                        'message': content,
                        'accepter': json_text_data['accepter'],
                        'type': json_text_data['type'],
                    }
                )
                await self.send_json({
                    'type': json_text_data['type'],
                    'message': content
                })
            #获取userlist
            if json_text_data['type'] == str(channel.user_list):
                print('user_list')
                allvalues = self.r.hvals(self.USER_SEEION)
                lists = []
                for item in allvalues:
                    try:
                        json_allvalues_data = json.loads(item)
                        listitem = UserList()
                        listitem.uid = json_allvalues_data['name']
                        listitem.session = json_allvalues_data['channel_name']
                        l = json.dumps(listitem, default=user_list_json)
                        print(l)
                        lists.append(l)

                        await self.send_json({
                            'type': 'userlist',
                            'message': lists
                        })
                    except Exception as e:
                        print(e)
            #发送单条消息给指定ID
            if json_text_data['type'] == str(channel.chat_solo):
                content = json_text_data['message']
                channelname = json_text_data['accepter']





        if(text_data == None and bytes_data != None):
            pass
        if(text_data != None and bytes_data != None):
            pass





    def getLocalIP(self):
        myname = socket.getfqdn(socket.gethostname())
        myaddr = socket.gethostname(myname)
        return myaddr