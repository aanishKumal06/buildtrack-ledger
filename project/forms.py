from django import forms
from .models import Project, ProjectMember


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "client_name",
            "start_date",
            "end_date",
            "status",
            "description",
            "actual_cost",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "client_name": forms.TextInput(attrs={"class": "form-control"}),
            "actual_cost": forms.NumberInput(attrs={"class": "form-control"}),
        }


class ProjectMemberForm(forms.ModelForm):
    class Meta:
        model = ProjectMember
        fields = ["project", "user", "role"]
        widgets = {
            "project": forms.Select(attrs={"class": "form-select"}),
            "user": forms.Select(attrs={"class": "form-select"}),
            "role": forms.Select(attrs={"class": "form-select"}),
        }
