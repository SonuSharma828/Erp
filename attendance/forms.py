from django import forms
from .models import Attendance
from core.models import AttendanceStatusType
class AttendanceForm(forms.ModelForm):
    status = forms.ModelChoiceField(queryset=AttendanceStatusType.objects.all())
    class Meta:
        model = Attendance
        fields = ['user', 'date', 'status', 'remarks']

