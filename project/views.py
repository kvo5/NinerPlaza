from django.shortcuts import render

def joinTeam(request):
    return render(request, 'join_team.html')

def profile(request):
    return render(request, 'profile.html') 