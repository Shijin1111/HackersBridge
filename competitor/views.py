from datetime import timedelta
from django import http
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
from django.http import HttpResponse, JsonResponse
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

def find_individual_events(request):
    individual_events = IndividualEvent.objects.all()
    return render(request,'competitor/find_individual_events.html',{"individual_events":individual_events})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from host.models import GroupEvent, TeamEnrollment, IndividualEvent
from .models import Team

@login_required
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

    return render(request, 'competitor/enroll_in_event.html', {'event': event, 'user_teams': user_teams ,"user_id": request.user.id })


import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404

def booking(request, event_id, user_id):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    event = get_object_or_404(GroupEvent, id=event_id)
    payment_data = {
        "amount": int(event.entry_fee * 100),  # Convert to paise
        "currency": "INR",
        "receipt": f"order_rcpt_{event_id}_{user_id}",
        "payment_capture": 1
    }
    order = client.order.create(data=payment_data)

    context = {
        "order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": event.entry_fee,
        "event": event,
    }
    return render(request, "competitor/payment.html", context)

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
    team = Team.objects.get(id=team_id)  # Fetch the team object
    return render(request, 'competitor/team_activities.html', {'team': team})

def schedules(request, team_id):
    return render(request, 'competitor/schedules.html', {'team_id': team_id})


def chat_box(request, team_id):
    return render(request, 'competitor/chat_box.html', {'team_id': team_id})

def meeting(request, team_id):
    return render(request, 'competitor/meeting.html', {'team_id': team_id})

def home(request):
    return render(request, 'competitor/home.html')

def schedules(request, team_id):
    sessions = Session.objects.filter(team_id=team_id).order_by('-date', '-time')
    return render(request, 'competitor/schedules.html', {'sessions': sessions, 'team_id': team_id})


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


from host.models import IndividualEvent, IndividualEnrollment
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now, make_aware
from datetime import timedelta
import pytz
from django.contrib import messages

# Define IST timezone
IST = pytz.timezone('Asia/Kolkata')

@login_required
def ind_event_dashboard(request, event_id):
    event = get_object_or_404(IndividualEvent, id=event_id)
    user = request.user
    
    has_attended = IndResult.objects.filter(user=user, event=event).exists()

    if has_attended:
        return render(request, 'competitor/ind_submitted.html')
    # Check if the user is already enrolled
    enrollment, created = IndividualEnrollment.objects.get_or_create(event=event, user=request.user)

    # Ensure enrolled_at is timezone-aware in IST
    if enrollment.enrolled_at is None:
        enrollment.enrolled_at = make_aware(now(), IST)  # Assign current IST time if null
        enrollment.save()

    # Convert enrolled_at to IST
    enrolled_at_ist = enrollment.enrolled_at.astimezone(IST)
    event_end_time = enrolled_at_ist + timedelta(minutes=event.time_duration)
    deadline = event.last_submission_datetime.astimezone(IST)
    current_time = now().astimezone(IST)

    print("Enrolled at (IST):", enrolled_at_ist)
    print("Current time (IST):", current_time)
    print("Event end time (IST):", event_end_time)

    if current_time > event_end_time or current_time > deadline:
        print("Redirecting because event has ended.")
        messages.error(request, "The event has ended. You can no longer participate.")
        return redirect('competitor:event_expired_page')

    problems = event.problems.all()  # Fetch related problems

    return render(request, 'competitor/ind_event_dashboard.html', {
    'event': event,
    'problems': problems,
    'event_end_time': event_end_time.strftime('%Y-%m-%dT%H:%M:%S')  # Send ISO format
})


    
def ind_event_expiry(request):
    return render(request, 'competitor/ind_event_expiry.html')
    
    
# problme execution logic -------------------------------------------------------------
import re

# Remove non-breaking spaces and cleanup input code
def sanitize_code(code):
    return re.sub(r'\u00A0', ' ', code)

def get_complete_code(problem, language, user_code):
    """
    Concatenate prefix, user code, and main section for execution.
    """
    prefix = getattr(problem, f"{language}_code_prefix", "") or ""
    main_code = getattr(problem, f"{language}_main", "") or ""

    return f"{prefix}\n{user_code}\n{main_code}"

from host.models import Problem
import subprocess,os
from .models import ProblemResult

def problem_details(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    results = []
    code = ""
    language = "python"
    testcases_passed = 0
    total_testcases = problem.test_cases.count()

    if request.method == 'POST':
        language = request.POST.get('language')
        code = request.POST.get('code')

        # Prepare the final code for execution
        complete_code = get_complete_code(problem, language, code)
        test_cases = problem.test_cases.all()

        for test_case in test_cases:
            user_input = test_case.input_data.strip()
            expected_output = test_case.expected_output.strip()
            output = ""
            success = False

            try:
                if language == 'python':
                    process = subprocess.run(
                        ['python3', '-c', complete_code],
                        input=user_input.encode(),
                        capture_output=True,
                        timeout=5
                    )
                    output = process.stdout.decode().strip()

                elif language == 'cpp':
                    sanitized_code = sanitize_code(complete_code)
                    with open('code.cpp', 'w') as f:
                        f.write(sanitized_code)

                    compile_process = subprocess.run(['g++', 'code.cpp', '-o', 'code.out'], capture_output=True)
                    if compile_process.returncode != 0:
                        output = compile_process.stderr.decode().strip()
                    else:
                        process = subprocess.run(['./code.out'], input=user_input.encode(), capture_output=True, timeout=5)
                        output = process.stdout.decode().strip()

                elif language == 'java':
                    with open('Main.java', 'w') as f:
                        f.write(complete_code)

                    compile_process = subprocess.run(['javac', 'Main.java'], capture_output=True)
                    if compile_process.returncode != 0:
                        output = compile_process.stderr.decode().strip()
                    else:
                        process = subprocess.run(['java', 'Main'], input=user_input.encode(), capture_output=True, timeout=5)
                        output = process.stdout.decode().strip()

            except subprocess.TimeoutExpired:
                output = "Execution timed out."
            
            success = (output == expected_output)
            if success:
                testcases_passed += 1 
            results.append({
                'test_case': test_case,
                'output': output,
                'expected_output': expected_output,
                'success': success
            })

        # Clean up temporary files
        for filename in ['code.cpp', 'code.out', 'Main.java', 'Main.class']:
            if os.path.exists(filename):
                os.remove(filename)
        # **Save the result if "Save Code" button was clicked**
        if 'save_result' in request.POST:
                problem_result, created = ProblemResult.objects.get_or_create(
                    user=request.user,
                    problem=problem,
                    defaults={'testcases_passed': testcases_passed, 'total_testcases': total_testcases}
                )

                if not created:
                    # If entry already exists, update the testcases_passed and total_testcases
                    problem_result.testcases_passed = testcases_passed
                    problem_result.total_testcases = total_testcases
                    problem_result.save()
                    
    return render(request, 'competitor/problem_details.html', {
        'problem': problem,
        'results': results,
        'code': code,
        'language': language
    })



from django.db.models import Sum
from host.models import IndividualEvent
from .models import ProblemResult, IndResult

@login_required
def submit_event(request, event_id):
    event = get_object_or_404(IndividualEvent, id=event_id)
    problems = event.problems.all()
    user = request.user

    passed_testcases = ProblemResult.objects.filter(user=user, problem__in=problems).aggregate(total_passed=Sum('testcases_passed'))['total_passed'] or 0

    ind_result, created = IndResult.objects.update_or_create(
        user=user,
        event=event,
        defaults={'passed_testcases': passed_testcases}
    )

    return redirect('/competitor/find_individual_events/')


def results(request):
    return render(request, 'competitor/results.html') 

def ind_results(request):
    individual_events = IndividualEvent.objects.filter(indresult__user=request.user)
    return render(request,'competitor/ind_results.html',{"individual_events":individual_events})

def ind_leaderboard(request,event_id):
    results = IndResult.objects.filter(event_id=event_id).order_by('-passed_testcases')
    return render(request, 'competitor/ind_leaderboard.html', {'results': results})

def group_results(request):
    group_events = GroupEvent.objects.all()
    return render(request,'competitor/group_results.html',{"group_events":group_events})

from host.models import HackathonGrading
def group_leaderboard(request,event_id):
    results = HackathonGrading.objects.filter(event_id=event_id).order_by('-overall_score')
    return render(request, 'competitor/group_leaderboard.html', {'results': results})

from .models import Team, ChatMessage

def chatbox(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    messages = ChatMessage.objects.filter(team=team).order_by("timestamp")  # Get previous messages
    return render(request, "competitor/chatbox.html", {"team": team, "messages": messages})

