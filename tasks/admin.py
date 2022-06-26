from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .forms import *
from .models import *

class TaskUserAdmin(ModelAdmin):
    list_display = ('text', 'date_end', 'visible', 'finished', 'author')

admin.site.register(Task, TaskUserAdmin)
