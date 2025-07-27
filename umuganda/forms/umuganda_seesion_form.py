from django import forms
from umuganda.models import UmugandaSession

class UmugandaSessionForm(forms.ModelForm):
    class Meta:
        model = UmugandaSession
        fields = ['date', 'sector']
