# Generated by Django 4.0.5 on 2022-06-29 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_subggwptask'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SubGGWPTask',
        ),
        migrations.AddField(
            model_name='subtask',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
