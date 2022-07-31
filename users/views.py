import random
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, View, TemplateView, DetailView, UpdateView
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from .forms import *
from tasks.views import AuthFormsMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail
from .utils import email_activation_token, reset_password_activation_token

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


class ActivateEmailSendView(LoginRequiredMixin, AuthFormsMixin, View):
    template_name = 'users/email_send.html'

    def get(self, request, *args, **kwargs):
        token = email_activation_token.make_token(request.user)
        uid64 = force_str(urlsafe_base64_encode(force_bytes(request.user.pk)))
        url = 'https://tasks-project-485.herokuapp.com' + reverse_lazy('activate_email', kwargs={'uidb64': uid64, 'token': token})

        send_mail('Email activation from "Tasks web site"', 
                  f'Hello {request.user.first_name}! Now you can activate your email, just follow the link: {url}', 
                  'djangoemailsends@gmail.com', [request.user.email,], 
                  fail_silently=False)
        context={'title': 'Email send'}
        context.update(self.get_simple_context())
        return render(request=request, template_name=self.template_name, context=context)


class ActivateEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and email_activation_token.check_token(user, token):
            user.email_active = True
            user.save()
            login(request, user)
            return redirect('email_success')
        else:
            return redirect('email_error')


class ActivateEmailSuccessView(AuthFormsMixin, TemplateView):
    template_name = 'users/email_success.html'
    extra_context = {'title': 'Email success'}


class ActivateEmailErrorView(AuthFormsMixin, TemplateView):
    template_name = 'users/email_error.html'
    extra_context = {'title': 'Email error'}


def LogoutView(request):
    logout(request)
    return redirect('home')


class ResetPassworEmailView(AuthFormsMixin, FormView):
    form_class = ResetPasswordEmailForm
    template_name = 'users/reset_pass_email.html'
    extra_context = {'title': 'Reset password'}

    def post(self, request, *args, **kwargs):
        form_email = request.POST['email']

        try:
            user = get_user_model().objects.get(email = form_email)
        except(get_user_model().DoesNotExist):
            user = None

        if user is not None:
            return HttpResponseRedirect(reverse_lazy('reset_pass_send', args=(form_email,)))
        else:
            return redirect('reset_pass_error')


class ResetPasswordSendView(AuthFormsMixin, View):
    template_name = 'users/reset_pass.html'

    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(email = kwargs['email'])
        token = reset_password_activation_token.make_token(user)
        uid64 = force_str(urlsafe_base64_encode(force_bytes(user.pk)))
        url = 'https://tasks-project-485.herokuapp.com' + reverse_lazy('reset_pass', kwargs={'uidb64': uid64, 'token': token})

        send_mail('Email activation from "Tasks web site"', 
                  f'Hello {user.first_name}! Now you can reset your password, just follow the link: {url}', 
                  'djangoemailsends@gmail.com', 
                  [user.email,], 
                  fail_silently=False)
        context={'title': 'Reset password'}
        context.update(self.get_simple_context())
        return render(request=request, template_name=self.template_name, context=context)


class ResetPasswordChangeView(AuthFormsMixin, View):
    template_name = 'users/reset_pass_change.html'
    form_class = SetPasswordForm

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and reset_password_activation_token.check_token(user, token):
            form = self.form_class(user)
            context={'title': 'Reset password', 'form': form, 'uidb64': uidb64, 'token': token}
            context.update(self.get_simple_context())
            return render(request=request, template_name=self.template_name, context=context)
        else:
            return redirect('reset_pass_error')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and reset_password_activation_token.check_token(user, token):
            form = self.form_class(user, request.POST)
            if form.is_valid():
                user.set_password(request.POST['new_password1'])
                user.save()
                return JsonResponse({'success_link': reverse_lazy('home')}, status=200)
            else:
                return JsonResponse({'form_errors': form.errors}, status=203)
        else:
            return JsonResponse({'error_link': reverse_lazy('reset_pass_error')}, status=203)


class ResetPasswordErrorView(AuthFormsMixin, TemplateView):
    template_name = 'users/reset_pass_error.html'
    extra_context = {'title': 'Reset password error'}


class UserDetailView(UserPassesTestMixin, LoginRequiredMixin, AuthFormsMixin, DetailView):
    template_name = 'users/detail.html'
    model = get_user_model()
    context_object_name = 'user_detail'
    extra_context = {'title': 'Profile'}
    
    def test_func(self):
        user_detail = get_user_model().objects.get(pk=self.kwargs['pk'])
        return self.request.user == user_detail


class UserChangePasswordView(UserPassesTestMixin, LoginRequiredMixin, AuthFormsMixin,  PasswordChangeView):
    template_name = 'users/change.html'
    form_class = SetPasswordForm
    extra_context = {'title': 'Change password', 'link_to_form': 'change_password'}

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return JsonResponse({'success_link': reverse_lazy('user_detail', args=(str(self.request.user.pk),))}, status=200)


    def form_invalid(self, form):
        return JsonResponse({'form_errors': form.errors}, status=203)


    def test_func(self):
        user_detail = get_user_model().objects.get(pk=self.kwargs['pk'])
        return self.request.user == user_detail


class UserChangeEmailView(UserPassesTestMixin, LoginRequiredMixin, AuthFormsMixin,  UpdateView):
    model = get_user_model()
    template_name = 'users/change.html'
    fields = ('email',)
    extra_context = {'title': 'Change email', 'link_to_form': 'change_email'}

    def form_valid(self, form):
        self.request.user.email_active = False
        self.request.user.save()
        form.save()
        return JsonResponse({'success_link': reverse_lazy('user_detail', args=(str(self.request.user.pk),))}, status=200)


    def form_invalid(self, form):
        return JsonResponse({'form_errors': form.errors}, status=203)


    def test_func(self):
        user_detail = get_user_model().objects.get(pk=self.kwargs['pk'])
        return self.request.user == user_detail


class UserChangeImageView(UserPassesTestMixin, LoginRequiredMixin, AuthFormsMixin,  UpdateView):
    model = get_user_model()
    template_name = 'users/change.html'
    fields = ('image',)
    extra_context = {'title': 'Change image', 'link_to_form': 'change_image'}

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success_link': reverse_lazy('user_detail', args=(str(self.request.user.pk),))}, status=200)


    def form_invalid(self, form):
        return JsonResponse({'form_errors': form.errors}, status=203)


    def test_func(self):
        user_detail = get_user_model().objects.get(pk=self.kwargs['pk'])
        return self.request.user == user_detail


class UserChangeNameView(UserPassesTestMixin, LoginRequiredMixin, AuthFormsMixin,  UpdateView):
    model = get_user_model()
    template_name = 'users/change.html'
    fields = ('first_name',)
    extra_context = {'title': 'Change name', 'link_to_form': 'change_name'}

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success_link': reverse_lazy('user_detail', args=(str(self.request.user.pk),))}, status=200)


    def form_invalid(self, form):
        return JsonResponse({'form_errors': form.errors}, status=203)


    def test_func(self):
        user_detail = get_user_model().objects.get(pk=self.kwargs['pk'])
        return self.request.user == user_detail