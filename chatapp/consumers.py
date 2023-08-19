from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
from chatapp.models import chatMessages, Friendship
from django.contrib.auth.models import User
from channels.db import DatabaseSyncToAsync
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import datetime
from asgiref.sync import async_to_sync

User = get_user_model()

class messagesConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the logged-in user and their chosen friend
        self.user = self.scope['user']
        self.friend_id = self.scope["url_route"]["kwargs"]["friend_id"]

        # Check if the logged-in user is friends with the chosen friend
        if await self.is_friend():
            self.room_name = f"chat_{min(self.user.id, int(self.friend_id))}_{max(self.user.id, int(self.friend_id))}"
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            print(self.room_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["messages"]


        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_name,
            {"type": "chat_message", "messages": message}
        )

    async def chat_message(self, event):
        message = event["messages"]
        await self.send(text_data=json.dumps({"messages": message}))

    async def is_friend(self):
        # Check if the logged-in user is friends with the chosen friend
        try:
            await DatabaseSyncToAsync(Friendship.objects.get)(
                Q(user=self.user, friend_id=self.friend_id, confirmed=True) |
                Q(user_id=self.friend_id, friend=self.user, confirmed=True)
            )
            return True
        except Friendship.DoesNotExist:
            return False

    async def save_message(self, message_content):
        # Save the message to the database
        sender = self.user
        receiver = await DatabaseSyncToAsync(User.objects.get)(id=self.friend_id)
        await DatabaseSyncToAsync(chatMessages.objects.create)(sender=sender, recipient=receiver, messages=message_content)


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
          self.close()
        
        self.group_name = f"notification_{self.user.id}"
        print(self.group_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.accept()
    
    async def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        data1 = json.loads(text_data)
        data = data1["notification Data"]
        print(data)
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
                 'type': 'send.notification',
                 'notification': data
        })   
    
    def send_notification(self, event):
        notification = event["notification"]
        print(notification)
        
        self.send(text_data=json.dumps({
            "notification": notification
        }))

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
        
#         if not self.user.is_authenticated:
#             await self.close()
        
#         self.group_name = f"notification_{self.user.id}"
#         print(self.group_name)
        
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
        
#         await self.accept()
    
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data=None, bytes_data=None):
#         print(text_data)
#         await self.channel_layer.group_send(self.room_name, {
#                  'type': 'send.notification',
#                  'notification': text_data
#         })   
    
#     async def send_notification(self, event):
#         notification = event["notification"]
        
#         await self.send(text_data=json.dumps({
#             "notification": notification
#         }))



       