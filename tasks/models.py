from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes


class Task(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField(default=timezone.now())
    text = models.CharField(max_length=50)
    finished = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)


    def get_progress(self):
        return (datetime.date.today() - self.date_start) / (self.date_end - self.date_start) * 100


    def __str__(self):
        return self.text