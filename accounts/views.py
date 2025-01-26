from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser  # Import your custom user model

def home(request):
    return render(request, 'home.html')

def host_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.user_type == 'host':
            login(request, user)
            return redirect('host:host_dashboard')
        else:
            return render(request, 'accounts/host_login.html', {'error': 'Invalid credentials or not a host.'})
    return render(request, 'accounts/host_login.html')

def competitor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.user_type == 'competitor':
            login(request, user)
            return redirect('competitor_dashboard')
        else:
            return render(request, 'accounts/competitor_login.html', {'error': 'Invalid credentials or not a competitor.'})
    return render(request, 'accounts/competitor_login.html')

def host_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        # Create a new user
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            user_type='host'  # Set user_type to 'host'
        )
        user.save()
        return redirect('host_login')
    return render(request, 'accounts/host_signup.html')

def competitor_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        # Create a new user
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            user_type='competitor'  # Set user_type to 'competitor'
        )
        user.save()
        return redirect('competitor_login')
    return render(request, 'accounts/competitor_signup.html')



@login_required
def competitor_dashboard(request):
    return render(request, 'accounts/competitor_dashboard.html')

