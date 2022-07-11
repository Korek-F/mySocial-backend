import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await print("DD")
    
    async def disconnect(self, code):
        await print("DIscornect")