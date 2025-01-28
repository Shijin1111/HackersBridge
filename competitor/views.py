from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home') 

@login_required
def competitor_dashboard(request):
    return render(request, "competitor/competitor_dashboard.html")

def my_teams(request):
    return render(request, "competitor/my_teams.html")


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Team, JoinRequest

def send_join_request(request, team_id, user_id):
    team = get_object_or_404(Team, id=team_id)
    user = get_object_or_404(User, id=user_id)

    try:
        team.send_join_request(user)
        return JsonResponse({'message': 'Join request sent successfully!'})
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

def manage_join_request(request, request_id, action):
    join_request = get_object_or_404(JoinRequest, id=request_id)
    
    if action == 'accept':
        join_request.accept()
        return JsonResponse({'message': 'Request accepted successfully!'})
    elif action == 'decline':
        join_request.decline()
        return JsonResponse({'message': 'Request declined successfully!'})
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)


# =================================================================================================
# =================================================================================================
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, JoinRequest
from .forms import TeamCreateForm

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamCreateForm(request.POST, user=request.user)
        if form.is_valid():
            team = form.save(commit=False)
            team.team_admin = request.user  # Set the logged-in user as the admin
            team.save()
            
            members = form.cleaned_data['members']
            for member in members:
                team.send_join_request(member)
            
            messages.success(request, 'Team created successfully, and join requests sent!')
            return redirect('competitor:my_teams') 
    else:
        form = TeamCreateForm(user=request.user)
    
    return render(request, 'competitor/create_team.html', {'form': form})
