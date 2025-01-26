from django.shortcuts import render, redirect
from .forms import GroupEventForm
from .models import GroupEvent

# @login_required
def host_dashboard(request):
    return render(request, 'host/host_dashboard.html')

def create_group_event(request):
    if request.method == "POST":
        print("POST request received.")  # Debugging line
        form = GroupEventForm(request.POST)
        if form.is_valid():
            print("Form is valid.")  # Debugging line
            GroupEvent.objects.create(
                hackathon_name=form.cleaned_data["hackathon_name"],
                organization=form.cleaned_data["organization"],
                theme=form.cleaned_data["theme"],
                frameworks=form.cleaned_data["frameworks"],
                max_team_size=form.cleaned_data["max_team_size"],
                last_submission_datetime=form.cleaned_data["last_submission_datetime"],
                evaluation_criteria=form.cleaned_data["evaluation_criteria"],
            )
            return render(request, "host/host_dashboard.html")
        else:
            print("Form errors:", form.errors)  # Debugging line for errors
    else:
        form = GroupEventForm()

    return render(request, "host/create_group_event.html", {"form": form})
