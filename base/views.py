from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
# from django.http import HttpResponse
from .models import Room, Topic, Message, User, Tutorial, Team, Competition
from .forms import RoomForm, UserForm, MyUserCreationForm, UserProfileForm, CompetitionForm

# Create your views here.

""" rooms = [
    {'id':1, 'name':'Lets Learn python!'},
    {'id':2, 'name':'Design with me'},
    {'id':3, 'name':'Frontend developers'},
] """

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('landing')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('landing')

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('landing')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()

    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    """ room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i """
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/recent_activity.html', context)

def fullProfile(request, pk=None):
    if pk:
        user = User.objects.get(id=pk)
    else:
        user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)

@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url = 'login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

def landing(request):
    # Get active competitions
    active_competitions = Competition.objects.filter(
        is_archived=False,
        deadline__gt=timezone.now()
    ).order_by('deadline')
    
    # Calculate statistics
    user_count = User.objects.count()
    competition_count = active_competitions.count()
    total_prize_pool = sum(comp.prize_pool for comp in active_competitions)
    
    context = {
        'user_count': user_count,
        'competition_count': competition_count,
        'total_prize_pool': int(total_prize_pool),  # Convert to integer for display
        'competitions': active_competitions
    }
    
    return render(request, 'landing.html', context)

def contactPage(request):
    return render(request, 'contact.html')

@login_required(login_url='login')
def like_tutorial(request, pk):
    try:
        tutorial = Tutorial.objects.get(id=pk)
        if request.user in tutorial.likes.all():
            tutorial.likes.remove(request.user)
        else:
            tutorial.likes.add(request.user)
        return redirect('tutorials')
    except Tutorial.DoesNotExist:
        messages.error(request, 'Tutorial not found')
        return redirect('tutorials')

def tutorialsPage(request):
    # Get or create the tutorials
    tutorial1, created1 = Tutorial.objects.get_or_create(
        id=1,
        defaults={
            'title': "How to Secure Funding for Your Startup",
            'description': "Learn the essential strategies for securing funding for your startup venture.",
            'video_url': "https://youtu.be/JhTeaJzZmSY"
        }
    )
    
    tutorial2, created2 = Tutorial.objects.get_or_create(
        id=2,
        defaults={
            'title': "How to Write a Business Plan",
            'description': "Master the art of writing an effective business plan for your startup.",
            'video_url': "https://youtu.be/G0GG8A3yuTE"
        }
    )
    
    tutorials = Tutorial.objects.all()
    context = {'tutorials': tutorials}
    return render(request, 'tutorials.html', context)

def termsPage(request):
    return render(request, 'terms.html')

def shopPage(request):
    return render(request, 'shop.html')

def team_shop(request, team_id):
    # Dictionary of team-specific products
    team_products = {
        '1': {  # EcoTech Solutions
            'products': [
                {'id': '1', 'name': 'Team Hoodie', 'price': '$45.00', 'image': 'team1_hoodie.jpg'},
                {'id': '2', 'name': 'Team T-Shirt', 'price': '$25.00', 'image': 'team1_tshirt.jpg'},
                {'id': '3', 'name': 'Team Keychain', 'price': '$10.00', 'image': 'team1_keychain.jpg'},
            ]
        },
        '2': {  # HealthHub
            'products': [
                {'id': '1', 'name': 'Team Hoodie', 'price': '$45.00', 'image': 'team2_hoodie.jpg'},
                {'id': '2', 'name': 'Team T-Shirt', 'price': '$25.00', 'image': 'team2_tshirt.jpg'},
                {'id': '3', 'name': 'Team Keychain', 'price': '$10.00', 'image': 'team2_keychain.jpg'},
            ]
        },
        '3': {  # FinTech Pioneers
            'products': [
                {'id': '1', 'name': 'Team Hoodie', 'price': '$45.00', 'image': 'team3_hoodie.jpg'},
                {'id': '2', 'name': 'Team T-Shirt', 'price': '$25.00', 'image': 'team3_tshirt.jpg'},
                {'id': '3', 'name': 'Team Keychain', 'price': '$10.00', 'image': 'team3_keychain.jpg'},
            ]
        },
        '4': {  # AI Innovators
            'products': [
                {'id': '1', 'name': 'Team Hoodie', 'price': '$45.00', 'image': 'team4_hoodie.jpg'},
                {'id': '2', 'name': 'Team T-Shirt', 'price': '$25.00', 'image': 'team4_tshirt.jpg'},
                {'id': '3', 'name': 'Team Keychain', 'price': '$10.00', 'image': 'team4_keychain.jpg'},
            ]
        }
    }
    
    team_data = team_products.get(str(team_id))
    return render(request, 'team_shop.html', {'team_data': team_data, 'team_id': team_id})

def product_detail(request, team_id, product_id):
    # Get product details from the team_products dictionary
    team_products = {
        '1': {  # EcoTech Solutions
            'products': [
                {'id': '1', 'name': 'Team Hoodie', 'price': '$45.00', 'image': 'team1_hoodie.jpg'},
                {'id': '2', 'name': 'Team T-Shirt', 'price': '$25.00', 'image': 'team1_tshirt.jpg'},
                {'id': '3', 'name': 'Team Keychain', 'price': '$10.00', 'image': 'team1_keychain.jpg'},
            ]
        },
        '2': {  # HealthHub
            'products': [
                {'id': '1', 'name': 'Team Hoodie', 'price': '$45.00', 'image': 'team2_hoodie.jpg'},
                {'id': '2', 'name': 'Team T-Shirt', 'price': '$25.00', 'image': 'team2_tshirt.jpg'},
                {'id': '3', 'name': 'Team Keychain', 'price': '$10.00', 'image': 'team2_keychain.jpg'},
            ]
        },
        '3': {  # FinTech Pioneers
            'products': [
                {'id': '1', 'name': 'Team Hoodie', 'price': '$45.00', 'image': 'team3_hoodie.jpg'},
                {'id': '2', 'name': 'Team T-Shirt', 'price': '$25.00', 'image': 'team3_tshirt.jpg'},
                {'id': '3', 'name': 'Team Keychain', 'price': '$10.00', 'image': 'team3_keychain.jpg'},
            ]
        },
        '4': {  # AI Innovators
            'products': [
                {'id': '1', 'name': 'Team Hoodie', 'price': '$45.00', 'image': 'team4_hoodie.jpg'},
                {'id': '2', 'name': 'Team T-Shirt', 'price': '$25.00', 'image': 'team4_tshirt.jpg'},
                {'id': '3', 'name': 'Team Keychain', 'price': '$10.00', 'image': 'team4_keychain.jpg'},
            ]
        }
    }
    
    team_data = team_products.get(str(team_id))
    if team_data is None:
        # Handle case when team is not found
        messages.error(request, 'Team not found')
        return redirect('shop')
        
    product = next((p for p in team_data['products'] if p['id'] == product_id), None)
    if product is None:
        # Handle case when product is not found
        messages.error(request, 'Product not found')
        return redirect('team-shop', team_id=team_id)
    
    return render(request, 'product_detail.html', {
        'product': product,
        'team_id': team_id
    })

@login_required(login_url='login')
def join_team(request):
    teams = Team.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        team_id = request.POST.get('team_id')
        
        if team_id:
            team = Team.objects.get(id=team_id)
            current_team = Team.objects.filter(members=request.user).first()
            
            if action == 'join':
                if team.get_member_count() < team.max_members:
                    # Remove user from current team if they're in one
                    if current_team and current_team != team:
                        current_team.members.remove(request.user)
                    
                    team.members.add(request.user)
                    messages.success(request, f'Successfully joined {team.name}!')
                else:
                    messages.error(request, 'This team is full!')
                    
            elif action == 'leave':
                team.members.remove(request.user)
                messages.success(request, 'Successfully left the team!')
        
        return redirect('join-team')
    
    context = {
        'teams': teams,
        'user_team': Team.objects.filter(members=request.user).first()
    }
    return render(request, 'join_team.html', context)

@login_required(login_url='login')
def profile(request, pk=None):
    if pk:
        user = User.objects.get(id=pk)
    else:
        user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'remove_resume':
            # Handle resume removal
            if request.user.resume:
                request.user.resume.delete()  # This deletes the file
                request.user.resume = None    # This removes the file reference
                request.user.save()
                messages.success(request, 'Resume removed successfully!')
            return redirect('edit-profile')
            
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'base/edit-profile.html', {'form': form})

@login_required(login_url='login')
def manage_competitions(request):
    if not request.user.is_sponsor:
        return redirect('landing')
        
    competitions = Competition.objects.filter(
        sponsor=request.user,
        is_archived=False
    ).order_by('deadline')
    
    if request.method == 'POST':
        form = CompetitionForm(request.POST, request.FILES)
        if form.is_valid():
            competition = form.save(commit=False)
            competition.sponsor = request.user
            competition.save()
            messages.success(request, 'Competition created successfully!')
            return redirect('manage-competitions')
    else:
        form = CompetitionForm()
    
    return render(request, 'base/manage_competitions.html', {
        'competitions': competitions,
        'form': form
    })

@login_required(login_url='login')
def edit_competition(request, pk):
    competition = get_object_or_404(Competition, id=pk, sponsor=request.user)
    
    if request.method == 'POST':
        form = CompetitionForm(request.POST, request.FILES, instance=competition)
        if form.is_valid():
            form.save()
            messages.success(request, 'Competition updated successfully!')
            return redirect('manage-competitions')
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='login')
def delete_competition(request, pk):
    competition = get_object_or_404(Competition, id=pk, sponsor=request.user)
    if request.method == 'POST':
        competition.delete()
        messages.success(request, 'Competition deleted successfully!')
    return redirect('manage-competitions')

@login_required(login_url='login')
def get_competition(request, pk):
    competition = get_object_or_404(Competition, id=pk, sponsor=request.user)
    data = {
        'name': competition.name,
        'deadline': competition.deadline.strftime('%Y-%m-%dT%H:%M'),
        'prize_pool': str(competition.prize_pool),
        'description': competition.description,
        'website_link': competition.website_link,
        'image_url': competition.image.url if competition.image else ''
    }
    return JsonResponse(data)