from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):
    # Custom field for Checkboxes
    WATER_USE_OPTIONS = [
        ('Irrigation', 'Irrigation'),
        ('Drinking', 'Drinking'),
        ('Tourism', 'Tourism'),
        ('None', 'None')
    ]
    existing_water_uses = forms.MultipleChoiceField(
        choices=WATER_USE_OPTIONS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Survey
        exclude = ['submitted_by', 'survey_date']
        widgets = {
            'seasonal_access_constraints': forms.Textarea(attrs={'rows': 2}),
            'qualitative_flow_desc': forms.Textarea(attrs={'rows': 2}),
            'known_clearances_needed': forms.Textarea(attrs={'rows': 2}),
            'social_sensitivities': forms.Textarea(attrs={'rows': 2}),
            'key_constraints': forms.Textarea(attrs={'rows': 2}),
        }

    # Clean method to convert the list of checkboxes into a string for the DB
    def clean_existing_water_uses(self):
        data = self.cleaned_data['existing_water_uses']
        return ", ".join(data)