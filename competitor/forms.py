from django import forms
from .models import Team
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamCreateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(user_type='competitor'),  # Filter competitors
        required=False,
        widget=forms.CheckboxSelectMultiple  # Use checkboxes for user selection
    )

    class Meta:
        model = Team
        fields = ['name', 'members']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the logged-in user
        super().__init__(*args, **kwargs)
        # Exclude the logged-in user from the members field
        self.fields['members'].queryset = self.fields['members'].queryset.exclude(id=user.id)
