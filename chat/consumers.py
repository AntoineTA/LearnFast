import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    groups = ['chat']

    async def connect(self):
        await self.accept()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        await self.channel_layer.group_send(
            'chat',
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
