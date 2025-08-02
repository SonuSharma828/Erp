from django import forms
from .models import Employee
from core.models import PhotoIdType

class EmployeeForm(forms.ModelForm):
    photo_id_type = forms.ModelChoiceField(queryset=PhotoIdType.objects.all(),widget=forms.Select(attrs={'class': 'w-full mt-2 px-4 py-2 border rounded-md'}))
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'joining_date': forms.DateInput(attrs={'type':'date'}),
            'photo_id_type': forms.Select(attrs={'class': 'w-full mt-2 px-4 py-2 border rounded-md'}),
        }
