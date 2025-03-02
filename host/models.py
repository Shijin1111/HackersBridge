from django.utils import timezone
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

# ------------------------------------------------------------------------

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    sample_testcases = models.TextField()

    python_code_prefix = models.TextField(blank=True, null=True)  # Allow blank/null
    python_function_signature = models.TextField(blank=True, null=True)
    python_main = models.TextField(blank=True, null=True)

    cpp_code_prefix = models.TextField(blank=True, null=True)
    cpp_function_signature = models.TextField(blank=True, null=True)
    cpp_main = models.TextField(blank=True, null=True)

    java_code_prefix = models.TextField(blank=True, null=True)
    java_function_signature = models.TextField(blank=True, null=True)
    java_main = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()

from django.db import models
from django.conf import settings

class IndividualEvent(models.Model):
    hackathon_name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    start_datetime = models.DateTimeField(auto_now_add=True)
    last_submission_datetime = models.DateTimeField()
    time_duration = models.IntegerField(help_text="Duration in minutes")  
    prize = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    problems = models.ManyToManyField('Problem', related_name="individual_events")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="individual_events")

    def __str__(self):
        return self.hackathon_name

class IndividualEnrollment(models.Model):
    event = models.ForeignKey('IndividualEvent', on_delete=models.CASCADE, related_name='enrollments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrolled_events')
    enrolled_at = models.DateTimeField(auto_now_add=True)  # Timestamp of enrollment
