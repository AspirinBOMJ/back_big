import random
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, View, TemplateView
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.urls import reverse_lazy
from .forms import *
from tasks.views import AuthFormsMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail

class SignUpView(View):
    form_class = CustomUserCreateForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'form_errors': form.errors}, status=203)


class LoginView(View):

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'authenticate_error': 'Your data not valid'}, status=203)
            

def LogoutView(request):
    logout(request)
    return redirect(reverse_lazy('home'))