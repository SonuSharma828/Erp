from django import forms
from .models import Empdata, EmployeePayment
from spp.mixins import TailwindFormMixin
from core.models import EmployeePaymentType,LeaveType
class UserForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = Empdata
        fields = '__all__'


class EmployeePaymentForm(TailwindFormMixin,forms.ModelForm):
    type = forms.ModelChoiceField(queryset=EmployeePaymentType.objects.all())
    class Meta:
        model = EmployeePayment
        exclude = ['approved','approval_status','approved_by','approved_at']
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'approved': forms.CheckboxInput(),
        }


from django import forms
from .models import LeaveRequest

class LeaveRequestForm(TailwindFormMixin,forms.ModelForm):
    leave_type = forms.ModelChoiceField(queryset=LeaveType.objects.all())
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']

class LeaveReviewForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status', 'reviewer_remarks']
