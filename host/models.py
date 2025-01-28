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
