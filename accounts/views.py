from django.shortcuts import render, HttpResponse, redirect
from .forms import SignupForm, SignInForm, ProfileUpdate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile

# Create your views here.
def singup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, "Password does not match.")
                return redirect('/')

            createUser = User.objects.create_user(username = username, password=password)
          

            # Verify reCAPTCHA
            print("vaild")
            print(form.cleaned_data['captcha'])
            messages.success(request, "account created successfully.")
            return redirect('singIn')
            
        else:
                messages.error(request, "reCAPTCHA verification failed.")
                return redirect('/')
    else:
         form = SignupForm()
         return render(request, "signUp.html",  {'form': form})
    
def signIn(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            # Perform form submission logic here
            # For example, create a user account
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'] 

            user = authenticate(request, username=username, password=password)
            if user is not None:
              login(request, user)
              messages.success(request, "Logged in successfully.")
              return redirect('chat/Home')  # Redirect to the appropriate page after login
            else:
                messages.error(request, "Invalid Username and Password.")
                return redirect('singIn')
            
        else:
            messages.error(request, "reCAPTCHA verification failed.")
            return redirect('singIn')
    else:
        form = SignInForm()
        return render(request, "signIn.html", {'form': form})

def hendle_logout(request):
    logout(request)
    return redirect("singIn")  

def profile(request):
    if request.method == 'POST':
        form = ProfileUpdate(request.POST, request.FILES) 
        if form.is_valid():
            img = form.cleaned_data['img']
            update = Profile.objects.get(user = request.user.id)
            update.pic=img
            update.save()
            messages.success(request, "Account created successfully.")
            return redirect('profile')
    else:
        form = ProfileUpdate()
    return render(request, "profile.html", {'form': form})
