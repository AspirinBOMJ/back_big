# Generated by Django 4.0.5 on 2022-06-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='active',
        ),
        migrations.AddField(
            model_name='customuser',
            name='email_active',
            field=models.BooleanField(default=False, verbose_name='User is active'),
        ),
    ]
