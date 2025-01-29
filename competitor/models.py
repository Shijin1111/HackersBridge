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


