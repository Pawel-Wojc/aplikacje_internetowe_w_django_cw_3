import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Channel, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        self.room_group_name = f'chat_{self.channel_id}'

        if not self.user.is_authenticated:
            await self.close()
            return

        self.chat_channel = await self.get_channel(self.channel_id)
        if not self.chat_channel:
            await self.close()
            return

        is_member = await self.is_member(self.chat_channel, self.user)
        if not is_member:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()

        if not message:
            return

        saved_message = await self.save_message(
            author=self.user,
            channel=self.chat_channel,
            content=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': saved_message.content,
                'author': self.user.username,
                'created_at': saved_message.created_at.strftime('%H:%M'),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'author': event['author'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def get_channel(self, channel_id):
        try:
            return Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            return None

    @database_sync_to_async
    def is_member(self, channel, user):
        return channel.members.filter(id=user.id).exists()

    @database_sync_to_async
    def save_message(self, author, channel, content):
        return Message.objects.create(
            author=author,
            channel=channel,
            content=content,
            message_type='text'
        )