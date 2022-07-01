from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .forms import *
from .models import *


class SubTaskInline(admin.TabularInline):
    model = SubTask


class TaskUserAdmin(ModelAdmin):
    inlines = [SubTaskInline]


admin.site.register(Task, TaskUserAdmin)
admin.site.register(SubTask)
