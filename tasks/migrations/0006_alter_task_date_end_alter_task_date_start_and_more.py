# Generated by Django 4.0.5 on 2022-06-29 11:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0005_alter_task_date_end_alter_task_date_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_end',
            field=models.DateField(default=datetime.date(2022, 6, 29)),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_start',
            field=models.DateField(default=datetime.date(2022, 6, 29)),
        ),
        migrations.AlterField(
            model_name='task',
            name='text',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
        ),
    ]
