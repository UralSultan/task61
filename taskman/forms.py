from django import forms
from .models import Project, Task
from .validators import validate_no_ban_words, validate_summary_length


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['start_date', 'end_date', 'title', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'type']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }

    def clean_summary(self):
        summary = self.cleaned_data.get('summary', '')
        validate_summary_length(summary)
        validate_no_ban_words(summary)
        return summary

    def clean_description(self):
        description = self.cleaned_data.get('description') or ''
        validate_no_ban_words(description)
        return description
