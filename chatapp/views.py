from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import chatMessages, Friendship, Notification
from django.contrib import messages
from django.db.models import Q
from accounts.models import Profile


# Create your views here.
def home(request):
    # # List of all users
    friends_as_user = Friendship.objects.filter(user=request.user, confirmed=True).values_list('friend', flat=True)
    friends_as_friend = Friendship.objects.filter(friend=request.user, confirmed=True).values_list('user', flat=True)
        
    all_friend_ids = set(friends_as_user) | set(friends_as_friend)

    friends = User.objects.filter(id__in=all_friend_ids)
    profile =  Profile.objects.filter(user__in=friends)
   
    if not profile.exists():
        context ={
            'error': 'No chat found..'
            }
        return render(request, "index.html", context)
    
    context ={
            'user':profile
            }
    return render(request, "index.html", context)
          
def chat_room(request, recipientId):
    friend = get_object_or_404(User, id=recipientId)
    messages = chatMessages.objects.filter(
        (Q(sender=request.user) & Q(recipient=friend)) |
        (Q(sender=friend) & Q(recipient=request.user))
    ).order_by('timestamp')

    context ={
      'recipientId': recipientId,
       'messages':messages,
       'friend_name':friend
    }
    return render(request, 'chatRoom.html', context)

def listUsers(request):
    # chek the user is exit in friend list 
    existing_friendships = Friendship.objects.filter(
        Q(user=request.user) | Q(friend=request.user)
    )
    friend_ids = set()
    for friendship in existing_friendships:
        friend_ids.add(friendship.user_id)
        friend_ids.add(friendship.friend_id)
    
    # Display the user is not friends and exclude current user logeed in 
    list_user =User.objects.exclude(
        Q(id=request.user.id) | Q(id__in=friend_ids)
    )

    profile = Profile.objects.filter(user__in = list_user)
  
    # new friend requests
    newRequest = Friendship.objects.filter(friend = request.user.id, confirmed=False)
    profiles = Profile.objects.filter(user__in=newRequest.values('user'))
    context ={
      'list_user':profile,
       'newRequest':profiles
    }
    return render(request, "listUser.html", context)


def send_friend_request(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    Friendship.objects.create(user=request.user, friend=friend)
    messages.success(request, f"Friend request sent to {friend.username}")
    return redirect('userLists')  # Redirect to your friend list view

def accept_friend_request(request, friend_id):
    friendship = Friendship.objects.get(user=friend_id, friend=request.user)
    friendship.confirmed = True
    friendship.save()
    messages.success(request, f"You are now friends with {friendship.user.username}")
    return redirect("userLists")

def notification(request):
    notificationList = Notification.objects.filter(user = request.user)
    context ={
        'notification':notificationList
    }
    return render(request, 'notification.html', context)