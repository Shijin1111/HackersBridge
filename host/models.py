from django.conf import settings
from django.db import models

class GroupEvent(models.Model):
    hackathon_name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    theme = models.CharField(max_length=200)
    frameworks = models.CharField(max_length=300)
    max_team_size = models.IntegerField()
    last_submission_datetime = models.DateTimeField()
    evaluation_criteria = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="group_events")


class TeamEnrollment(models.Model):
    event = models.ForeignKey('GroupEvent', on_delete=models.CASCADE, related_name='enrollments')
    team = models.ForeignKey('competitor.Team', on_delete=models.CASCADE, related_name='enrolled_events')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team.name} enrolled in {self.event.hackathon_name}"

from django.conf import settings
from django.db import models
from competitor.models import Team  # Import Team model from competitor app

class ProjectSubmission(models.Model):
    event = models.ForeignKey('GroupEvent', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # Now this will work
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    live_link = models.URLField(max_length=200, blank=True, null=True)
    files = models.ManyToManyField('File', blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team.name} - {self.event.hackathon_name} Submission"

class File(models.Model):
    file = models.FileField(upload_to='project_files/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} uploaded at {self.upload_time}"
