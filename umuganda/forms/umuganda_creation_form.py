from django import forms
from umuganda.models import UmugandaSession
from datetime import date as dt, timedelta

class UmugandaSessionForm(forms.ModelForm):
    class Meta:
        model = UmugandaSession
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.sector = kwargs.pop('sector', None)
        super().__init__(*args, **kwargs)

    def clean_date(self):
        date = self.cleaned_data.get('date')

        if not date:
            return date

        if date < dt.today():
            raise forms.ValidationError("Umuganda date cannot be in the past.")

        if self.sector:
            recent_session = (
                UmugandaSession.objects
                .filter(sector=self.sector)
                .order_by('-date')
                .first()
            )

            if recent_session:
                days_since_last = (date - recent_session.date).days
                if days_since_last < 29:
                    raise forms.ValidationError(
                        f"An Umuganda was already scheduled on {recent_session.date}. "
                        f"You must wait at least 29 days before assigning a new one."
                    )

        return date
        