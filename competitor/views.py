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
    teams = Team.objects.filter(members=request.user)
    print("Logged-in user:", request.user)
    print("Teams found:", teams)
    return render(request, "competitor/my_teams.html",{"teams":teams})


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

# ===============================================================================================
# ===============================================================================================
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import JoinRequest

@login_required
def view_join_requests(request):
    # Get all pending join requests for the logged-in user
    pending_requests = JoinRequest.objects.filter(user=request.user, status='pending')

    return render(request, 'competitor/view_join_requests.html', {'pending_requests': pending_requests})

@login_required
def accept_join_request(request, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id)

    # Make sure the logged-in user is the one requested to join
    if join_request.user != request.user:
        messages.error(request, "You are not authorized to accept this join request.")
        return redirect('competitor:my_teams')

    # Update the join request status to accepted
    join_request.status = 'accepted'
    join_request.save()

    # Add the user to the team
    team = join_request.team
    team.members.add(join_request.user)

    messages.success(request, f"Join request accepted for {team.name}.")
    return redirect('competitor:my_teams')
@login_required
def reject_join_request(request, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id)

    # Make sure the logged-in user is the one requested to join
    if join_request.user != request.user:
        messages.error(request, "You are not authorized to reject this join request.")
        return redirect('competitor:my_teams')

    # Update the join request status to rejected
    join_request.status = 'rejected'
    join_request.save()

    messages.success(request, f"Join request rejected for {join_request.team.name}.")
    return redirect('competitor:my_teams')
