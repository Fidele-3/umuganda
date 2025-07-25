from django import forms
from umuganda.models import UmugandaSession
from users.models.addresses import Village

class UmugandaSessionForm(forms.ModelForm):
    class Meta:
        model = UmugandaSession
        fields = ['village', 'tools_needed', 'description', 'fines_policy']
        widgets = {
            'tools_needed': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'fines_policy': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        cell = kwargs.pop('cell', None)
        super().__init__(*args, **kwargs)
        if cell:
            self.fields['village'].queryset = Village.objects.filter(cell=cell)
