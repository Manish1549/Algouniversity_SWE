from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
# Create your views here.



def registration(request) :
    if request.user.is_authenticated:
        return redirect('/home/')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password match check
        if password != confirm_password :
            messages.error(request,'Passwords do not match.')
            return redirect('/auth/register/')
        # Username and email uniqueness checks
        if User.objects.filter(username=username).exists() :
            messages.error(request,'Username already taken.')
            return redirect('/auth/register/')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('/auth/register/')
        
        #Cretae User
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        messages.info(request,'User registered succesfully')
        return redirect('/auth/register/')
    #For GET request
    return render(request, "register.html",{})

def login_user(request):
    if request.method =='POST' :
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        # Try to find user by email first
        try:
            user_obj = User.objects.get(email=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            username = identifier

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.info(request,'invalid credentials')
            return redirect('/auth/login/')
        login(request,user)
        messages.info(request,'login succesful')
        return(redirect('Homepage'))
    
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.info(request,'Logout Successful')
    return redirect('/auth/login/')



