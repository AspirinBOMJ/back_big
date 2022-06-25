from dataclasses import fields
import email
from pyexpat import model
from statistics import mode
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.contrib.auth import get_user_model


class CustomUserCreateForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Account name')
    first_name = forms.CharField(max_length=20, label='Name')
    password1 = forms.CharField(widget = forms.TextInput(attrs={'type':'password'}), label = "Password")
    password2 = forms.CharField(widget = forms.TextInput(attrs={'type':'password'}), label = "Password again")
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'first_name', 'email', 'image')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('first_name', 'email', 'image', 'email_active')


class ResetPasswordEmailForm(forms.Form):
    email = forms.EmailField(label="Enter your email")


class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('password',)