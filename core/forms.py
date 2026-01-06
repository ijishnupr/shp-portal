from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        exclude = ['submitted_by', 'created_at']
        widgets = {
            'reason_for_rejection': forms.Textarea(attrs={'rows': 3}),
        }