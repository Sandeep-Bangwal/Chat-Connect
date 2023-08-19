from django import forms
from captcha.fields import ReCaptchaField

class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-control form-control-sm'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'form-control form-control-sm'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter confirm password ', 'class': 'form-control form-control-sm'}))
    captcha = ReCaptchaField()

class SignInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-control form-control-sm'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Passwords', 'class': 'form-control form-control-sm'}))
    captcha = ReCaptchaField() 

class ProfileUpdate(forms.Form):
    img = forms.ImageField()    


