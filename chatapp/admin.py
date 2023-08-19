from django.contrib import admin
from .models import chatMessages, Friendship, Notification

@admin.register(chatMessages)
class chatMessagesAdmin(admin.ModelAdmin):
    list_display = ['sender','recipient','messages','timestamp']

admin.site.register(Friendship) 

@admin.register(Notification)
class chatMessagesAdmin(admin.ModelAdmin):
    list_display = ['user','send_by','notification_msg','is_seen','created']
