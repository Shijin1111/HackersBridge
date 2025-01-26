from django import forms

class GroupEventForm(forms.Form):
    hackathon_name = forms.CharField(
        max_length=200,
        label="Hackathon Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Hackathon Name"}),
    )
    organization = forms.CharField(
        max_length=200,
        label="Hosting Organization",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Organization Name"}),
    )
    theme = forms.CharField(
        max_length=200,
        label="Theme",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Theme of Hackathon"}),
    )
    frameworks = forms.CharField(
        max_length=300,
        label="Frameworks to Follow",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Frameworks (comma-separated)"}),
    )
    max_team_size = forms.IntegerField(
        label="Max Team Size",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter Maximum Team Size"}),
    )
    last_submission_datetime = forms.DateTimeField(
        label="Last Date & Time for Submission",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
    )
    evaluation_criteria = forms.CharField(
        label="Evaluation Criteria",
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter Evaluation Criteria"}),
    )
