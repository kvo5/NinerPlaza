from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, Competition
from django.utils import timezone
# from django.contrib.auth.models import User

class MyUserCreationForm(UserCreationForm):
    is_sponsor = forms.BooleanField(required=False, label='Are you a sponsor?')
    
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2', 'is_sponsor']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'avatar', 'headline', 'bio', 'location', 
                 'website', 'github', 'linkedin', 'resume']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'headline': forms.TextInput(attrs={'placeholder': 'Your professional headline'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://'}),
            'github': forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username'}),
            'resume': forms.FileInput(attrs={
                'accept': '.pdf',
                'class': 'resume-upload'
            }),
        }

class CompetitionForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
    )
    
    class Meta:
        model = Competition
        fields = ['name', 'image', 'deadline', 'prize_pool', 'description', 'website_link']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'prize_pool': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website_link': forms.URLInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now():
            raise forms.ValidationError("Deadline cannot be in the past")
        return deadline