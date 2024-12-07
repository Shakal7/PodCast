from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate
from .froms import *


# Create your views here.

def Explore(request):
    return render(request, 'Explore.html')


def home(request):
    # If the user is not authenticated, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect('msg')

    # Ensure the user has a profile
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    # Check if the user clicked "More" (pass a query parameter like ?view=all)
    view_all = request.GET.get('view') == 'all'

    # Fetch free episodes (default behavior)
    episodes = Episode.objects.filter(is_premium=False)

    # Show all episodes only if "More" is clicked and user is premium or creator
    if view_all and (request.user.profile.is_premium or request.user.profile.is_creator):
        episodes = Episode.objects.all()

    context = {
        'episodes': episodes,
        'view_all': view_all,  # Add this flag to handle UI changes
    }
    return render(request, 'home.html', context)


def signUpCreator(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        if password == confirmPassword and len(password) >= 3:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
            profile = Profile.objects.create(user=user, is_creator=True)
            profile.save()
            return redirect('/')

    # return redirect('login')
    return render(request, 'signup.html')


def signUpListener(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        if password == confirmPassword and len(password) >= 3:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
            return redirect('/')

    # return redirect('login')
    return render(request, 'signup.html')


def signUpPremium(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        if password == confirmPassword and len(password) >= 3:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
            profile = Profile.objects.create(user=user, is_premium=True)
            profile.save()
            return redirect('/')

    # return redirect('login')
    return render(request, 'pre_signup.html')


def signup_view(request):
    user_role = request.user.role  # Assumes the user model has a role attribute
    return render(request, 'signup.html', {'user_role': user_role})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to 'home' instead of '/'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')  # Get 'next' parameter if available
            return redirect(next_url or 'home')  # Redirect to 'next' or 'home'
        else:
            messages.error(request, "Invalid username or password!")  # Add error message

    return render(request, 'login.html')


def logOut(request):
    auth.logout(request)
    return redirect('/')


def upload_episode(request):
    user = request.user

    # Assuming Profile model has a OneToOneField with User model
    try:
        profile = user.profile  # Retrieve the profile associated with the user
    except Profile.DoesNotExist:
        # Handle the case where the profile doesn't exist (optional)
        profile = None

    if profile and profile.is_creator:
        form = EpisodeForm()

        if request.method == 'POST':
            form = EpisodeForm(request.POST, request.FILES)
            if form.is_valid():
                # Assuming the episode model is being created and associated with the user
                episode = form.save(commit=False)
                episode.creator = request.user  # Assign the current user as the creator
                episode.save()
                return redirect('home')  # Redirect to home page after successful form submission

    else:
        # Handle the case where the user does not have a creator profile
        form = None  # or provide appropriate feedback to the user

    context = {
        'form': form
    }
    return render(request, 'upload_episode.html', context)


def delete_epi(request, id):
    epi = Episode.objects.get(pk=id)
    if request.method == 'POST':
        epi.delete()
        return redirect('home')
    context = {'epi': epi}

    return render(request, template_name='delete_epi.html', context=context)


def player(request, id):
    player = Episode.objects.get(pk=id)
    context = {
        'player': player,
    }
    return render(request, template_name='audio.html', context=context)


def mock_payment(user):
    user.subscription.plan = 'Premium'
    user.subscription.is_active = True
    user.subscription.end_date = timezone.now() + timedelta(days=30)
    user.subscription.save()


def activate_premium(request):
    if request.method == 'POST':
        mock_payment(request.user)
        messages.success(request)
        return redirect('home')


def more_option(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Ensure the user has a profile
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    # Fetch episodes based on user type
    if request.user.profile.is_premium or request.user.profile.is_creator:
        # Fetch all episodes for premium users or creators
        episodes = Episode.objects.all()
    else:
        # Restrict to free episodes for regular users
        episodes = Episode.objects.filter(is_premium=False)

    context = {
        'episodes': episodes,
        'is_more_page': True,  # Add this to indicate the request is for the more page
    }
    return render(request, 'home.html', context)


def search_episodes(request):
    query = request.GET.get('s', '')  # Get the query from the search form
    # Use Title instead of title
    episodes = Episode.objects.filter(Title__icontains=query) if query else Episode.objects.all()
    return render(request, 'home.html', {'episodes': episodes, 'query': query})


def message(request):
    return render(request, 'msg.html')
