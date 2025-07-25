from django.forms.widgets import ClearableFileInput

class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True




from django import forms
from admn.models.respond import Respond

class RespondForm(forms.ModelForm):
    media_file = forms.FileField(
        required=False,
        widget=MultiFileInput(attrs={'multiple': True}),
        label="Upload media (images, videos, or documents)",
    )

    class Meta:
        model = Respond
        fields = ['message', 'status', 'concerned_sector']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your response here...'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'concerned_sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Local Police'}),
        }
