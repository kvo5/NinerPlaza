# Generated by Django 5.1.1 on 2024-12-06 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_remove_user_resume_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='education',
        ),
        migrations.RemoveField(
            model_name='user',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='user',
            name='skills',
        ),
    ]
