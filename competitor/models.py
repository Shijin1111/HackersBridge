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
