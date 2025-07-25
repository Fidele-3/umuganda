from django import forms
from users.models.addresses import Province, District, Sector as AddressSector
from sector.models import AdminSector
import uuid
from django.core.exceptions import ObjectDoesNotExist

class sectorCreateForm(forms.ModelForm):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), required=True)
    district = forms.ModelChoiceField(queryset=District.objects.none(), required=True)
    sector = forms.ModelChoiceField(queryset=AddressSector.objects.none(), required=True)

    class Meta:
        model = AdminSector
        fields = ['province', 'district', 'sector']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.is_bound:
            province_id = self.data.get('province')
            if province_id:
                self.fields['district'].queryset = District.objects.filter(province_id=province_id)
            else:
                self.fields['district'].queryset = District.objects.none()

            district_id = self.data.get('district')
            if district_id:
                self.fields['sector'].queryset = AddressSector.objects.filter(district_id=district_id)
            else:
                self.fields['sector'].queryset = AddressSector.objects.none()

        elif self.instance and self.instance.pk:
            try:
                province = self.instance.province
                self.fields['district'].queryset = District.objects.filter(province=province)
            except ObjectDoesNotExist:
                self.fields['district'].queryset = District.objects.none()

            try:
                district = self.instance.district
                self.fields['sector'].queryset = AddressSector.objects.filter(district=district)
            except ObjectDoesNotExist:
                self.fields['sector'].queryset = AddressSector.objects.none()

        else:
            self.fields['district'].queryset = District.objects.none()
            self.fields['sector'].queryset = AddressSector.objects.none()
