from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View, CreateView
from users.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from .models import *

class AuthFormsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup'] = CustomUserCreateForm()
        context['login'] = AuthenticationForm()
        return context

    def get_simple_context(self):
        context = {}
        context['signup'] = CustomUserCreateForm()
        context['login'] = AuthenticationForm()
        return context

    
class TaskListView(AuthFormsMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    extra_context = {'title': 'List'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['finished_list'] = self.model.objects.all().filter(finished=True, visible=True)
        context['unfinished_list'] = self.model.objects.all().filter(finished=False, visible=True)
        return context


class TaskProfileListView(UserPassesTestMixin, LoginRequiredMixin, AuthFormsMixin, ListView):
    model = Task
    template_name = 'tasks/list_profile.html'
    extra_context = {'title': 'Your list'}

    def test_func(self):
        user_detail = get_user_model().objects.get(pk=self.kwargs['pk'])
        return self.request.user == user_detail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user_model().objects.get(pk=self.kwargs['pk'])
        context['finished_list'] = self.model.objects.all().filter(finished=True, author=user)
        context['unfinished_list'] = self.model.objects.all().filter(finished=False, author=user)
        return context


class TasCreationView(LoginRequiredMixin, AuthFormsMixin, ListView):
    model = Task
    template_name = 'tasks/create_task.html'
    fields = ('text', 'date_end', 'visible')

    