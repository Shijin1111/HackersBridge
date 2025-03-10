from pyexpat.errors import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .forms import GroupEventForm
from .models import GroupEvent,ProjectSubmission

def logout_view(request):
    logout(request)
    return redirect('home')  

@login_required
def host_dashboard(request):
    user_group_events = GroupEvent.objects.filter(created_by=request.user) 
    print(now()) 
    return render(request, "host/host_dashboard.html", {"group_events": user_group_events})

from django.utils import timezone

def create_group_event(request):
    if request.method == "POST":
        form = GroupEventForm(request.POST)
        if form.is_valid():
            GroupEvent.objects.create(
                hackathon_name=form.cleaned_data["hackathon_name"],
                organization=form.cleaned_data["organization"],
                theme=form.cleaned_data["theme"],
                frameworks=form.cleaned_data["frameworks"],
                max_team_size=form.cleaned_data["max_team_size"],
                last_submission_datetime=form.cleaned_data["last_submission_datetime"],
                evaluation_criteria=form.cleaned_data["evaluation_criteria"],
                created_by=request.user,  
            )
            return redirect("host:host_dashboard")  
        else:
            print("Form errors:", form.errors)
    else:
        form = GroupEventForm()
    return render(request, "host/create_group_event.html", {"form": form})

from django.utils import timezone

def finished_group_events(request):
    # Get the current time in IST by converting UTC to local time
    current_time_ist = timezone.localtime(timezone.now())
    
    finished_events = GroupEvent.objects.filter(
        created_by=request.user,
        last_submission_datetime__lt=current_time_ist  # Compare with IST
    )
    return render(request, 'host/finished_group_events.html', {'finished_events': finished_events})

def live_events(request):
    # Get the current time in IST by converting UTC to local time
    current_time_ist = timezone.localtime(timezone.now())
    
    live_events = GroupEvent.objects.filter(
        created_by=request.user,
        last_submission_datetime__gte=current_time_ist  # Compare with IST
    )
    return render(request, 'host/live_events.html', {'live_events': live_events})


@login_required
def view_submissions(request, event_id):
    event = get_object_or_404(GroupEvent, id=event_id)
    submissions = ProjectSubmission.objects.filter(event=event)

    return render(request, 'host/view_submissions.html', {
        'event': event,
        'submissions': submissions
    })

from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import File

def download_file(request, file_id):
    # Retrieve the file instance by its ID
    file_instance = get_object_or_404(File, id=file_id)

    # Open the file and return it as a response for download
    response = FileResponse(open(file_instance.file.path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
    return response


from django.shortcuts import render, redirect
from .forms import IndividualEventForm

def create_individual_event(request):
    if request.method == "POST":
        form = IndividualEventForm(request.POST)
        if form.is_valid():
            individual_event = form.save(commit=False)
            individual_event.created_by = request.user
            individual_event.save()
            form.save_m2m()  # Save Many-to-Many relationships
            return redirect('host:host_dashboard')  # Redirect to host dashboard after submission
    else:
        form = IndividualEventForm()
    
    return render(request, 'host/create_individual_event.html', {'form': form})



from django.shortcuts import render, get_object_or_404, redirect
from .models import HackathonGrading, ProjectSubmission
from .forms import HackathonGradingForm

def grade_project(request, submission_id):
    submission = get_object_or_404(ProjectSubmission, id=submission_id)
    
    # Check if a grade already exists for this submission
    grading, created = HackathonGrading.objects.get_or_create(team=submission.team, event=submission.event)

    if request.method == "POST":
        form = HackathonGradingForm(request.POST, instance=grading)
        if form.is_valid():
            form.save()
            grading.calculate_total_score()  # Update overall score
            return redirect('host:view_submissions', event_id=submission.event.id)
    else:
        form = HackathonGradingForm(instance=grading)

    return render(request, "host/grade_project.html", {"form": form, "submission": submission})
