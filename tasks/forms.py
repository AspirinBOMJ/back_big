from django import forms
from .models import *


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('text', 'date_end', 'visible')


    def __init__(self, *args, **kwargs):
        self.user = kwargs['user']
        self.slug = kwargs['slug']
        super(TaskCreationForm, self).__init__(*args, **kwargs)
    

    def save(self, commit=True):
        new_task = Task.objects.update_or_create(slug=self.slug,
                                                 author=self.user,
                                                 time=self.cleaned_data.get('date_end'),
                                                 text=self.cleaned_data.get('text'),
                                                 visible=self.cleaned_data.get('visible'))
        return new_task