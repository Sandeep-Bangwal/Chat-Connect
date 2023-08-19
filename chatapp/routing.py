from django.urls import path
from .consumers import messagesConsumers, NotificationConsumer


websocket_urlpatterns = [
    path('wc/chatMessages/<friend_id>', messagesConsumers.as_asgi()),
    path('wc/notification', NotificationConsumer.as_asgi()),
  
]