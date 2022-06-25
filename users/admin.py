from pyexpat import model
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import *


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreateForm
    form = CustomUserChangeForm
    list_display = ['username', 'first_name', 'email', 'email_active', 'image']


admin.site.register(CustomUser)
