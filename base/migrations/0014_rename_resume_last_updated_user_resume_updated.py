# Generated by Django 5.1.1 on 2024-12-06 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_remove_user_last_updated_user_resume_last_updated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='resume_last_updated',
            new_name='resume_updated',
        ),
    ]