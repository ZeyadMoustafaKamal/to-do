from django import forms

class Signup(forms.Form):
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

# I will make anther class for the login page because I don't want to use the same class for both sign up and login

class Login(forms.Form):
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput(),label='Password')

# This is for verification

class Verify(forms.Form):
    code = forms.CharField(label='Enter the code please')