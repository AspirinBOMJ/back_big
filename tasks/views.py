import email
from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from users.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
import six

class AuthFormsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup'] = CustomUserCreateForm()
        context['login'] = AuthenticationForm()
        return context
    

class HomeView(AuthFormsMixin, TemplateView):
    template_name = 'tasks/home.html'
    extra_context = {'title': 'Home'}
    