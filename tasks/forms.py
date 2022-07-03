from dataclasses import field, fields
from pyexpat import model
from random import choices
from django import forms
from .models import *

class SortTasksForm(forms.Form):
    CHOICES = (
    ('date_descending', 'Sort by date descending'),
    ('date_ascending', 'Sort by date ascending'))

    choices = forms.ChoiceField(choices=CHOICES, label='')


class SubTaskForm(forms.ModelForm):
    text = forms.CharField(max_length=30, label='Create new subtask')
    class Meta:
        model = SubTask
        fields = ['text',] 


class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=30, label='Create new comment', )
    class Meta:
        model = Comment
        fields = ['text',] 