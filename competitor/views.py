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
from django.contrib.auth.models import User

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

def find_group_events(request):
    group_events = GroupEvent.objects.all()
    return render(request,'competitor/find_group_events.html',{"group_events":group_events})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from host.models import GroupEvent, TeamEnrollment
from .models import Team

def enroll_in_event(request, event_id):
    event = get_object_or_404(GroupEvent, id=event_id)
    user_teams = Team.objects.filter(team_admin=request.user)  # Teams created by the user

    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        team = get_object_or_404(Team, id=team_id, team_admin=request.user)
        
        # Check if the team is already enrolled
        if TeamEnrollment.objects.filter(event=event, team=team).exists():
            messages.error(request, f"{team.name} is already enrolled in this event!")
        else:
            # Enroll the team
            TeamEnrollment.objects.create(event=event, team=team)
            messages.success(request, f"{team.name} successfully enrolled in {event.hackathon_name}!")
        return redirect('competitor:find_group_events')

    return render(request, 'competitor/enroll_in_event.html', {'event': event, 'user_teams': user_teams})


def enrolled_hackathons(request):
    # Get all teams the user is part of (either as team_admin or member)
    user_teams = Team.objects.filter(members=request.user) | Team.objects.filter(team_admin=request.user)
    
    # Get all enrollments for these teams
    enrolled_events = TeamEnrollment.objects.filter(team__in=user_teams).select_related('event')
    
    return render(request, 'competitor/enrolled_hackathons.html', {'enrolled_events': enrolled_events})


def event_details(request, event_id, team_id):
    event = get_object_or_404(GroupEvent, id=event_id)
    team = get_object_or_404(Team, id=team_id)

    # Ensure the team is actually enrolled in the event
    enrollment = TeamEnrollment.objects.filter(event=event, team=team).first()
    if not enrollment:
        return render(request, 'competitor/not_allowed.html', {"message": "You are not enrolled in this event."})

    return render(request, 'competitor/event_details.html', {'event': event, 'team': team})


# views.py in competitor app
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from host.models import ProjectSubmission, File, GroupEvent
from competitor.models import Team
from django.core.files.storage import default_storage

@login_required
def submit_project(request, event_id):
    event = GroupEvent.objects.get(id=event_id)
    team = Team.objects.filter(members=request.user).first()

    if not team:
        return redirect('competitor:my_teams')

    if request.method == 'POST':
        live_link = request.POST.get('live_link', '').strip()
        uploaded_file = request.FILES.get('project_files')  # Get the uploaded ZIP file

        if uploaded_file and uploaded_file.name.endswith('.zip'):
            # Create a ProjectSubmission or update it if it already exists
            project_submission, created = ProjectSubmission.objects.get_or_create(
                event=event, team=team, submitted_by=request.user
            )
            project_submission.live_link = live_link
            project_submission.save()

            # Handle the uploaded ZIP file
            file_instance = File.objects.create(file=uploaded_file)
            project_submission.files.add(file_instance)

            return redirect('competitor:enrolled_hackathons')
        else:
            # Handle the case where the file isn't a ZIP file
            error_message = "Please upload a valid ZIP file."
            return redirect('competitor:enrolled_hackathons')
        
    return redirect('competitor:enrolled_hackathons')

def team_activities(request, team_id):
    return render(request, 'competitor/team_activities.html', {'team_id': team_id})


def schedules(request, team_id):
    return render(request, 'competitor/schedules.html', {'team_id': team_id})

def chat_box(request, team_id):
    return render(request, 'competitor/chat_box.html', {'team_id': team_id})

def meeting(request, team_id):
    return render(request, 'competitor/meeting.html', {'team_id': team_id})

def home(request):
    return render(request, 'competitor/home.html')

def schedule_view(request, team_id):
    sessions = Session.objects.filter(team_id=team_id).order_by('-date', '-time')
    return render(request, 'competitor/schedule.html', {'sessions': sessions, 'team_id': team_id})


from django.shortcuts import render, redirect
from .models import Session, Team
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django import forms

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'date', 'time']

@login_required
def add_session(request, team_id):
    team = Team.objects.get(id=team_id)

    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.team = team
            session.organizer = request.user
            session.save()
            return redirect('competitor:schedules', team_id=team.id)
    else:
        form = SessionForm()

    return render(request, 'competitor/add_session.html', {'form': form, 'team': team})
