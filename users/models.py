from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email_active = models.BooleanField(default=False, verbose_name='User is active')
    image = models.ImageField(upload_to='media', verbose_name='Image')
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
