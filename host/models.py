from django.db import models

class GroupEvent(models.Model):
    hackathon_name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    theme = models.CharField(max_length=200)
    frameworks = models.CharField(max_length=300)
    max_team_size = models.IntegerField()
    last_submission_datetime = models.DateTimeField()
    evaluation_criteria = models.TextField()

    def __str__(self):
        return self.hackathon_name
