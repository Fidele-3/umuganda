from django import forms
from umuganda.models import CellUmugandaSession
from users.models.addresses import Village

class CellUmugandaSessionForm(forms.ModelForm):
    class Meta:
        model = CellUmugandaSession
        fields = ['village', 'tools_needed', 'description', 'fines_policy']
        widgets = {
            'tools_needed': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        cell = kwargs.pop('cell', None)
        super().__init__(*args, **kwargs)
        if cell:
            self.fields['village'].queryset = Village.objects.filter(cell=cell)
