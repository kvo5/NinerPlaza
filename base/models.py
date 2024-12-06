from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os

def resume_upload_path(instance, filename):
    # Generate a path for the resume file
    ext = filename.split('.')[-1]
    return f'resumes/{instance.username}/resume.{ext}'

def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    return value

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    headline = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    resume_updated = models.DateTimeField(null=True, blank=True)
    is_sponsor = models.BooleanField(default=False)  # Added sponsor status

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.pk:  # If this is an update
            old_instance = User.objects.get(pk=self.pk)
            if old_instance.resume != self.resume:  # If resume has changed
                self.resume_updated = timezone.now()
        super().save(*args, **kwargs)

class TeamMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['joined_at']

class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=200, default='team1.jpg')  # Store image filename
    max_members = models.IntegerField(default=10)
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, through='TeamMembership', related_name='teams')
    
    def get_member_count(self):
        return self.members.count()
    
    def get_members_by_join_date(self):
        return self.members.order_by('teammembership__joined_at')
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    video_url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='tutorial_likes', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class Competition(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competitions')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='competitions/', default='default_competition.jpg')
    deadline = models.DateTimeField()
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    website_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['deadline']  # Sort by deadline

    def is_ending_soon(self):
        time_left = self.deadline - timezone.now()
        return time_left.days <= 7  # Competition ending within 7 days

    def save(self, *args, **kwargs):
        if self.deadline < timezone.now():
            self.is_archived = True
        super().save(*args, **kwargs)