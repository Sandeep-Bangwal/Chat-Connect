from django.urls import path
from . import views

urlpatterns = [
   path('', views.singup, name='singup'),
   path('singIn', views.signIn , name='singIn'),
   path('logout', views.hendle_logout , name='logout'),
   path('profile', views.profile , name='profile')
   
   
]