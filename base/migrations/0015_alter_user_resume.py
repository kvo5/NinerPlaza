# Generated by Django 5.1.1 on 2024-12-06 09:26

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_rename_resume_last_updated_user_resume_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to=base.models.resume_upload_path),
        ),
    ]