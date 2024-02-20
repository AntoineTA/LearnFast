import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from main.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    groups = ['chat']

    @database_sync_to_async
    def log_message(self, message, author):
        author = User.objects.get(username=author)
        Message.objects.create(author=author, content=message)

    async def connect(self):
        await self.accept()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author = text_data_json['author']
        timestamp = text_data_json['timestamp']
        await self.log_message(message, author)
        # author = await database_sync_to_async(User.objects.get)(username=text_data_json['author'])

        # await database_sync_to_async(Message.objects.create)(author=author, content=message)

        await self.channel_layer.group_send(
            'chat',
            {
                'type': 'chat_message',
                'message': message,
                'author': author,
                'timestamp': timestamp
            }
        )

    # Receive message from group
    async def chat_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'author': event['author'],
            'timestamp': event['timestamp']
        }))
