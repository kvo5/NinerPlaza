# Generated by Django 5.1.1 on 2024-12-06 11:51

import base.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_user_is_sponsor_alter_user_resume_competition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competition',
            old_name='description',
            new_name='caption',
        ),
        migrations.RenameField(
            model_name='competition',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='competition',
            old_name='website_url',
            new_name='website_link',
        ),
        migrations.AlterField(
            model_name='competition',
            name='deadline',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='competition',
            name='image',
            field=models.ImageField(default='competitions/default.jpg', upload_to='competitions/'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='prize_pool',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to=base.models.resume_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), base.models.validate_file_size]),
        ),
    ]
