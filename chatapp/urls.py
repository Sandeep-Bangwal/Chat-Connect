from django.urls import path
from . import views

urlpatterns = [
  path('Home', views.home, name='home'),
  path('chat_room/<int:recipientId>', views.chat_room, name='chat_room'),
  path('userLists', views.listUsers, name='userLists'),
  path('send_friend_request/<friend_id>', views.send_friend_request, name='send_friend_request'),
  path('accept_friend_request/<friend_id>', views.accept_friend_request, name='accept_friend_request'),
    path('notification', views.notification, name='notification'),
   
]