from dataclasses import field
from pyexpat import model
from random import choices
from django import forms
from .models import *

class SortTasksForm(forms.Form):
    CHOICES = (
    ('date_descending', 'Sort by date descending'),
    ('date_ascending', 'Sort by date ascending'))

    choices = forms.ChoiceField(choices=CHOICES, label='')
