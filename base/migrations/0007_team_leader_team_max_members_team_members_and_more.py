# Generated by Django 5.1.1 on 2024-11-21 16:54

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_team_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_teams', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='max_members',
            field=models.IntegerField(default=6, validators=[django.core.validators.MaxValueValidator(6)]),
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='teams', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='team',
            name='image',
            field=models.ImageField(null=True, upload_to='team_images/'),
        ),
        migrations.CreateModel(
            name='TeamJoinRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='join_requests', to='base.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'team')},
            },
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
