# Generated by Django 5.1.1 on 2024-12-06 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_rename_description_competition_caption_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='image',
            field=models.ImageField(default='competition-default.jpg', upload_to='competitions/'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='prize_pool',
            field=models.IntegerField(),
        ),
    ]