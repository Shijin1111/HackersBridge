from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def host_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.user_type == 'host':
            login(request, user)
            return redirect('host_dashboard')
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

@login_required
def host_dashboard(request):
    return render(request, 'accounts/host_dashboard.html')

@login_required
def competitor_dashboard(request):
    return render(request, 'accounts/competitor_dashboard.html')

