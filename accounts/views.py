from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from .models import UserProfile
import random
from django.core.mail import send_mail
from .forms import *

def signup(request):
    # I want to use it in the operation of sending 6 digit code
    global email,userprofile

    # if the user is already logged in
    if request.user.is_authenticated:
        if UserProfile.objects.get(user=request.user).verified:
            return redirect('index')
        else:
            return redirect('verify')
    

    if request.method == 'POST':
        form = Signup(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # if the email is exists show an error
            if User.objects.filter(email=email).first():
                messages.error(request, 'This E-mail is already exists')
            else:

                # first create the user instance and then create UserProfile instance
                
                user = User.objects.create(username = email, email = email, password = password)
                user.save()
                userprofile = UserProfile(user=user)
                userprofile.save()
                auth.login(request,user)
                return redirect('verify')
        else:
            # The user can change the attribute required
            messages.error(request,'Please check the fields and try again')
    else:
        form = Signup()
                
    return render(request,'accounts/signup.html',{'form':form})
def login(request):
    if request.user.is_authenticated :
        # I can show an error and make the form disappear but I think that redirect to the home page is better
        # First I didn't use this if stetement but It causes an issue because the user may not be verified but he may created an account so the request.use.is_authenticated will return True 
        if UserProfile.objects.get(user=request.user).verified:
            return redirect('index')
    
    if request.method == 'POST':

        form = Login(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email = email,password = password).first()
            if user is not None:
                auth.login(request,user)
                return redirect('index')
            else:
                # If the email or the password are not correct 
                messages.error(request,'Incorrect E-mail or password')
        else:
            messages.error(request,'Please check the fields and try again')
    else:
        form = Login()

    return render(request,'accounts/login.html',{'form':form})
def logout(request):

    # This is a simple function just log the user out
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')
def verify(request):
    userprofile = UserProfile.objects.filter(user=request.user).first()

    if request.user.is_authenticated:
        if UserProfile.objects.get(user=request.user).verified:
            return redirect('index')

    if request.method == 'POST':

        form = Verify(request.POST)

        # if the code is correct
        if form.is_valid():

            if form.cleaned_data['code'] == str(userprofile.code):
                userprofile.verified = True
                userprofile.code = 0
                userprofile.save()
                return redirect('index')
            else:
                messages.error(request,'Invalid code')
        else:
            messages.error(request,'Please check the fields and try again')
    else:
        form = Verify()
    if userprofile.code == 0:
        code = random.randint(100000,999999)
        subject = 'Here is the code to verify your E-mail'
        userprofile.code = code
        userprofile.save()
        message = f'Hello verify your E-mail using this code {userprofile.code}'
        send_mail(from_email='zmoustafa988@gmail.com', subject=subject, message=message, recipient_list=[email])
    
    return render(request,'accounts/email_verify.html',{'form':form})
