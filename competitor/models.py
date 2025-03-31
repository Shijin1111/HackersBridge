from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()  

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    team_admin = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='admin_teams'
    )  # The user who created the team (must be a competitor)
    members = models.ManyToManyField(
        User, 
        related_name='team_members', 
        blank=True
    ) 
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation

    def __str__(self):
        return self.name

    def add_member(self, user):
        """Add a user to the team if they are a competitor."""
        if user.user_type == 'competitor':  # Check if the user is a competitor
            self.members.add(user)

    def remove_member(self, user):
        """Remove a user from the team."""
        self.members.remove(user)

    def is_member(self, user):
        """Check if a user is a member of the team."""
        return self.members.filter(id=user.id).exists()

    def save(self, *args, **kwargs):
        """Ensure the team_admin is a competitor before saving the team."""
        if self.team_admin.user_type != 'competitor':
            raise ValueError("Only competitors can create teams.")
        super().save(*args, **kwargs)
    def send_join_request(self, user):
        """Send a join request to a user."""
        if self.is_member(user):
            raise ValueError("User is already a member of the team.")
        if self.join_requests.filter(user=user, status=JoinRequest.PENDING).exists():
            raise ValueError("A join request is already pending for this user.")
        
        JoinRequest.objects.create(team=self, user=user)

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JoinRequest(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        """Accept the join request and add the user to the team."""
        if self.status == self.PENDING:
            self.status = self.ACCEPTED
            self.save()
            self.team.members.add(self.user)

    def decline(self):
        """Decline the join request."""
        if self.status == self.PENDING:
            self.status = self.DECLINED
            self.save()

    def __str__(self):
        return f"Request from {self.user} to join {self.team}"


class ChatMessage(models.Model):
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]  # Messages appear in chronological order


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Session(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="sessions")
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.title} - {self.date} {self.time}"

from django.db import models
from django.apps import apps  # Import apps module for lazy import

class ProblemResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey("host.Problem", on_delete=models.CASCADE)  # Use "appname.ModelName"
    testcases_passed = models.IntegerField(default=0)
    total_testcases = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}: {self.testcases_passed}/{self.total_testcases}"

class IndResult(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    event = models.ForeignKey('host.IndividualEvent',on_delete=models.CASCADE)
    passed_testcases = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.event} - {self.passed_testcases} Passed"
    
    
from django.db import models
from host.models import GroupEvent
from django.conf import settings

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(GroupEvent, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')])
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.hackathon_name} - {self.status}"
