from django import forms
from .models import Team,Session
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


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'date', 'time']

    # Optional: Add custom labels and placeholders
    title = forms.CharField(
        max_length=255, 
        label='Session Title', 
        widget=forms.TextInput(attrs={'placeholder': 'Enter session title'})
    )
    date = forms.DateField(
        label='Session Date', 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    time = forms.TimeField(
        label='Session Time', 
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
