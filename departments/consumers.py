import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message, UserStatus

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if self.user.is_authenticated:
            # 1. Individual Room (for private messages)
            self.room_group_name = f"user_{self.user.id}"
            # 2. Global Group (for online/offline notifications)
            self.status_group_name = "staff_status_updates"

            # Join both groups
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.channel_layer.group_add(self.status_group_name, self.channel_name)

            await self.accept()
            
            # Update database to Online
            await self.update_user_status(True)

            # Broadcast to everyone else that this user is now Online
            await self.channel_layer.group_send(
                self.status_group_name,
                {
                    'type': 'user_online_notification',
                    'username': self.user.username,
                    'user_id': self.user.id
                }
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Update database to Offline
            await self.update_user_status(False)

            # Leave groups
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            await self.channel_layer.group_discard(self.status_group_name, self.channel_name)

    # --- RECEIVE FROM BROWSER ---
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        receiver_id = data.get('receiver_id')

        if message and receiver_id:
            # Save message to Database
            await self.save_message(self.user.id, receiver_id, message)

            # Send message to the receiver's private room
            await self.channel_layer.group_send(
                f"user_{receiver_id}",
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': self.user.id,
                    'sender_name': self.user.username
                }
            )

    # --- HANDLERS (Sending to Browser) ---

    # Handle private messages
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'private_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name']
        }))

    # Handle global online notifications
    async def user_online_notification(self, event):
        # Don't send the notification to the person who just logged in
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'user_status_update',
                'username': event['username'],
                'status': 'online'
            }))

    # --- DATABASE OPERATIONS ---

    @database_sync_to_async
    def update_user_status(self, online):
        status, created = UserStatus.objects.get_or_create(user=self.user)
        status.is_online = online
        status.save()

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        Message.objects.create(sender=sender, receiver=receiver, content=content)