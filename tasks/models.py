from django.db import models
from django.contrib.auth import get_user_model
import datetime
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.utils.encoding import force_str, force_bytes


class Task(models.Model):
    slug = models.TextField(unique=True, null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_start = models.DateField(default=datetime.date.today())
    date_end = models.DateField(default=datetime.date.today())
    text = models.CharField(max_length=200)
    finished = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)


    def get_progress(self):
        return (datetime.date.today() - self.date_start) / (self.date_end - self.date_start) * 100


    def __str__(self):
        return self.text


    def get_absolute_url(self):
        return reverse('task_detail', kwargs={"slug": self.slug})


class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.CharField(max_length=30)
    finished = models.BooleanField(default=False)


    def __str__(self):
        return self.text


    def get_absolute_url(self):
        return reverse('task_detail', kwargs={"slug": self.task.slug})
