import math
from os import remove
from pydoc import visiblename
from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View, CreateView, FormView, DeleteView, DetailView, UpdateView
from users.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from .utils import create_slug_for_task
import datetime
from .models import *
from .forms import *
from project import settings
import datetime
from django.template.loader import render_to_string

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



class TasksUpdateMixin:
    def get(self, request, *args, **kwargs):
        all_unfinished_tasks = Task.objects.all().filter(finished=False)
        for task in all_unfinished_tasks:
            if task.date_end <= datetime.date.today():
                task.finished = True
                task.save()
        return super().get(request, *args, **kwargs)


class TaskListView(AuthFormsMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    extra_context = {'title': 'List'}
    form_class = SortTasksForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['finished_list'] = self.model.objects.all().filter(finished=True, visible=True)
        context['unfinished_list'] = self.model.objects.all().filter(finished=False, visible=True)
        context['sort_form'] = self.form_class()
        return context


class TaskProfileListView(UserPassesTestMixin, LoginRequiredMixin, AuthFormsMixin, TasksUpdateMixin, ListView):
    model = Task
    template_name = 'tasks/list_profile.html'
    extra_context = {'title': 'Your list'}
    form_class = SortTasksForm

    def test_func(self):
        user_detail = get_user_model().objects.get(pk=self.kwargs['pk'])
        return self.request.user == user_detail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user_model().objects.get(pk=self.kwargs['pk'])
        context['finished_list'] = self.model.objects.all().filter(finished=True, author=user)
        context['unfinished_list'] = self.model.objects.all().filter(finished=False, author=user)
        context['sort_form'] = self.form_class()
        context['subtask_form'] = SubTaskForm()
        return context


class SortTaskHandlerView(View):
    form_class = SortTasksForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            choice = request.POST['choices']
            match choice:
                case 'date_descending':
                    tasks = Task.objects.all().order_by('-date_start')
                case 'date_ascending':
                    tasks = Task.objects.all().order_by('date_start')

            if self.kwargs['finished'] == 'True':
                tasks = tasks.filter(finished=True)
            else:
                tasks = tasks.filter(finished=False)
            
            if self.kwargs['profile'] == 'True':
                tasks = tasks.filter(author=request.user)
            else:
                tasks = tasks.filter(visible=True)

            html = ''
            for task in tasks:
                if self.kwargs['profile'] == 'True':
                    html += render_to_string('tasks/task.html', context={'task': task, 'profile': True, 'subtask_form': SubTaskForm()}, request=request)
                else:
                    html += render_to_string('tasks/task.html', context={'task': task,}, request=request)

            return JsonResponse({'html': html, 'finished': self.kwargs['finished']}, status=200)
        else:
            return JsonResponse({'form_errors': form.errors}, status=203)
        

class PleaseActivateView(AuthFormsMixin, TemplateView):
    template_name = 'tasks/please_activate.html'
    extra_context = {'title': 'Please activate your email'}


class TaskCreationView(LoginRequiredMixin, AuthFormsMixin, TasksUpdateMixin, CreateView):
    model = Task
    template_name = 'tasks/task_create.html'
    fields = ('text', 'date_end', 'visible')
    extra_context = {'title': 'Create task'}
    
    def get(self, request, *args, **kwargs):
        if request.user.email_active:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('please_activate')


    def form_valid(self, form):
        date = self.request.POST['date_end']
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        if date <= datetime.date.today():
            return JsonResponse({'form_errors': {'date': 'Date must be not today or early'}}, status=203)

        try:
            visible = self.request.POST['visible']
        except:
            visible = False

        if visible == 'on':
            visible = True
        task = Task.objects.create(author=self.request.user, text=self.request.POST['text'], date_end=self.request.POST['date_end'], visible=visible)
        task.slug = create_slug_for_task(task.pk, task.author.pk)
        task.save()
        return JsonResponse({'success_link': reverse_lazy('profile_list', args=(self.request.user.pk,))}, status=200)


    def form_invalid(self, form):
        return JsonResponse({'form_errors': form.errors}, status=203)
        

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, AuthFormsMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    extra_context = {'title': 'Delete'}


    def get_success_url(self):
        return reverse_lazy('profile_list', args=(self.request.user.pk,))


    def test_func(self):
        user = Task.objects.get(slug=self.kwargs['slug']).author
        return self.request.user == user


class TaskDetailView(AuthFormsMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task_detail'
    extra_context = {'title': 'Detail'}


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtask_form'] = SubTaskForm()
        context['comment_form'] = CommentForm()
        return context


    def get(self, request, *args, **kwargs):
        if not self.get_object().visible and self.get_object().author != request.user:
            return redirect('list')

        return super().get(request, *args, **kwargs)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, AuthFormsMixin, UpdateView):
    model = Task
    fields = ['text', 'date_end', 'visible']
    template_name = 'tasks/task_update.html'
    extra_context = {'title': 'Update'}

    def test_func(self):
        user = self.model.objects.get(slug=self.kwargs['slug']).author
        return self.request.user == user


    def post(self, request, *args, **kwargs):
        task = self.model.objects.get(slug=self.kwargs['slug'])
        if request.POST['date_end'] <= task.date_start:
            return JsonResponse({'form_errors': {'Date': 'To early'}}, status=203)


    def get(self, request, *args, **kwargs):
        task = self.model.objects.get(slug=self.kwargs['slug'])
        if task.finished:
            self.fields = ['text', 'visible']
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_slug'] = self.kwargs['slug']
        return context


    def form_valid(self, form):
        form.save()
        return JsonResponse({'success_link': reverse_lazy('task_detail', args=(self.kwargs['slug'],))}, status=200)


    def form_invalid(self, form):
        return JsonResponse({'form_errors': form.errors}, status=203)

class SubTaskCreateView(LoginRequiredMixin, UserPassesTestMixin, View):

    def post(self, request, *args, **kwargs):
        form = SubTaskForm(request.POST)
        if form.is_valid():
            text = request.POST['text']
            task = Task.objects.get(slug=self.kwargs['slug'])
            subtask = SubTask.objects.create(text=text, task=task)
            html = render_to_string('tasks/subtask.html', context={'subtask': subtask, 'profile': True}, request=request)
            return JsonResponse({'subtask_html': html, 'task_slug': self.kwargs['slug'], 'pk': subtask.pk}, status=200)
        else:
            return JsonResponse({'form_errors': form.errors, 'task_slug': self.kwargs['slug']}, status=203)


    def test_func(self):
        user = Task.objects.get(slug=self.kwargs['slug']).author
        return self.request.user == user

    
class SubTaskActivateView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        subtask = SubTask.objects.get(pk = self.kwargs['pk'])
        if subtask.finished:
            subtask.finished = False
        else:
            subtask.finished = True
        subtask.save()
        html = render_to_string('tasks/subtask.html', context={'subtask': subtask, 'profile': True}, request=request)
        return JsonResponse({'subtask_finished_html': html, 'pk': self.kwargs['pk']}, status=200)


    def test_func(self):
        user = SubTask.objects.get(pk=self.kwargs['pk']).task.author
        return self.request.user == user


class SubTaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        SubTask.objects.get(pk = self.kwargs['pk']).delete()
        return JsonResponse({'pk': self.kwargs['pk']}, status=200)
        

    def test_func(self):
        user = SubTask.objects.get(pk=self.kwargs['pk']).task.author
        return self.request.user == user


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            text = request.POST['text']
            task = Task.objects.get(slug=self.kwargs['slug'])
            author = request.user
            comment = Comment.objects.create(author=author, task=task, text=text)
            html = render_to_string('tasks/comment.html', context={'comment': comment, 'profile': True}, request=request)
            return JsonResponse({'comment_html': html, 'task_slug': self.kwargs['slug'], 'pk': comment.pk}, status=200)
        else:
            return JsonResponse({'form_errors': form.errors, 'task_slug': self.kwargs['slug']}, status=203)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, AuthFormsMixin, View):
    def get(self, request, *args, **kwargs):
        Comment.objects.get(pk = self.kwargs['pk']).delete()
        return JsonResponse({'pk': self.kwargs['pk']}, status=200)
        

    def test_func(self):
        user = Comment.objects.get(pk=self.kwargs['pk']).author
        return self.request.user == user


class HomeView(TemplateView):
    template_name = 'tasks/home.html'
    extra_context = {'title': 'Home'}
