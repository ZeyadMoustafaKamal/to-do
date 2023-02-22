from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Create your views here.

def signup(request):

    if 'btnsubmit' in request.POST:
        email = request.POST['email']
        password = request.POST['password']

        # if the email and password fields are empty show an error ( the user can delete required attribute in inspect mode )

        if email == '' or password == '':
            messages.error(request, 'Please check the fields and try again')
        
        else:
            # if the email is exists show an error
            if User.objects.filter(email=email).first():
                messages.error(request, 'This E-mail is already exists')
            else:
                # first create the user instance and then create UserProfile instance
                try:
                    # check if the user entered a valid E-mail
                    validate_email(email)
                    user = User.objects.create(username = email, email = email, password = password)
                    user.save()
                    userprofile = UserProfile(user=user)
                    userprofile.save()
                    auth.login(request,user)
                    return redirect('index')
                except ValidationError:
                    # show error if W-mail isn't valid
                    messages.error(request,'Make sure that you wrote a correct E-mail')
                
                
    return render(request,'accounts/signup.html')
def login(request):
    if request.user.is_authenticated:
        # I can show an error and make the form disappear but I think that redirect to the home page is better
        return redirect('index')
    
    if request.method == 'POST' and 'btnsubmit' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        # again check if the email and passward are not empty
        if email == '' or password == '':
            messages.error(request, 'Please check the fields and try again')
        else:
            # I tried to use auth.authenticate() , but it shows an error
            # I think that the error that I am using email and password ... not username and password to check if the user is exists or not 
            # when I started to develop this app I used this to create an instance for the Use model user = User(email=email,password=password)
            # this shows an error while creating the second user because django puts a default value for the username if I didn't pass it and I can't use the same name twice for the username
            # I can solve it by using user = User(username=email,password=password) 

            user = User.objects.filter(email=email,password=password).first()
            if user is not None:
                auth.login(request,user)
                return redirect('index')
            else:
                # If the email or the password are not correct 
                messages.error(request,'Error while loggin into your account')
    return render(request,'accounts/login.html')
def logout(request):

    # this is a simple function to use
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')