from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .forms import *
from .models import *


class SubTaskInline(admin.TabularInline):
    model = SubTask


class CommentInline(admin.TabularInline):
    model = Comment

class TaskUserAdmin(ModelAdmin):
    inlines = [SubTaskInline, CommentInline]


admin.site.register(Task, TaskUserAdmin)
admin.site.register(SubTask)
admin.site.register(Comment)
