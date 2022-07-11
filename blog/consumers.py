import json 
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

class NotificationsConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope.get('user')
        await self.accept()
        self.room_name = 'noti_'+user.username

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

    async def receive_json(self, content):
        print("Ds")
        await self.channel_layer.group_send(
            self.room_name,
            {
                "test":"test"
            }
        )

    async def websocket_message(self, event):
        print("YY")
        await self.send_json(({
            "test":"test2"
        }))


    async def send_status(self, event):
        print("SEND STATUs")
        await self.send_json({"payload":event})


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )