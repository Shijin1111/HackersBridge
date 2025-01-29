from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .forms import GroupEventForm
from .models import GroupEvent

def logout_view(request):
    logout(request)
    return redirect('home')  

@login_required
def host_dashboard(request):
    user_group_events = GroupEvent.objects.filter(created_by=request.user)  # Fetch events by logged-in user
    return render(request, "host/host_dashboard.html", {"group_events": user_group_events})

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

def finished_group_events(request):
    finished_events = GroupEvent.objects.filter(created_by=request.user,last_submission_datetime__lt=now())
    return render(request, 'host/finished_group_events.html', {'finished_events': finished_events})

def live_events(request):
    live_events = GroupEvent.objects.filter(created_by=request.user, last_submission_datetime__gte=now())
    return render(request, 'host/live_events.html', {'live_events': live_events})