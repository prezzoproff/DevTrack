from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True) #Adding the email field

    class meta:
        model = User
        fields = ['username', 'email', 'password', ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "phone"]

class TwoFactorForm(forms.Form):
    otp = forms.CharField(label="Enter OTP", max_length=6, required=True)