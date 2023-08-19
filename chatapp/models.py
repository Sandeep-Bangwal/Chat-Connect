from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

#chat-messages model
class chatMessages(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="recipient", on_delete=models.CASCADE)
    messages = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='user_friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_friendships', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)


    class Meta:
        unique_together = ['user', 'friend']

    def __str__(self):
        return f'{self.user.username} - {self.friend.username}' 
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    send_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sendBy")
    notification_msg = models.TextField()
    is_seen = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)    

@receiver(post_save, sender=Friendship)
def send_notification(sender, instance,created , **kwargs):
    if created and not instance.confirmed:
        sender_user = instance.user
        recipient_user = instance.friend
        data = {}
        data['msg']=f"You have a new friend request from {sender_user}"
        Notification.objects.create(user = recipient_user, send_by = sender_user,  notification_msg = f"You have a new friend request from {sender_user}")
        data['count'] = Notification.objects.filter(user=recipient_user, is_seen = False).count()
        
        print("Notification Data:", data)
        # Send real-time notification to the recipient using WebSocket consumer
        channel_layer = get_channel_layer() 
        async_to_sync(channel_layer.group_send)(
            f"notification_{recipient_user.id}",
            {
                'type': 'send.notification',
                'notification': json.dumps(data)
            }
        )
    if not created:
        sender_user = instance.user
        recipient_user = instance.friend
        data = {}
        data['msg']=f"{recipient_user} accept your friend request"
        Notification.objects.create(user = sender_user, send_by = recipient_user,  notification_msg = f"{recipient_user} accept your friend request")
        data['count'] = Notification.objects.filter(user=sender_user, is_seen = False).count()
        
        print("Notification Data:", data)
        # Send real-time notification to the recipient using WebSocket consumer
        channel_layer = get_channel_layer() 
        async_to_sync(channel_layer.group_send)(
            f"notification_{sender_user.id}",
            {
                'type': 'send.notification',
                'notification': json.dumps(data)
            }
        )










