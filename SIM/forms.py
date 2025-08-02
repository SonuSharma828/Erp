from django import forms
from .models import DailyStatus, ExpenseApproval, PaymentFollowUp, QuickJob
from .mixins import TailwindFormMixin
from core.models import TaskStatus,ExpenseType

class DailyStatusForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = DailyStatus
        fields = '__all__'

class PaymentFollowUpForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = PaymentFollowUp
        fields = '__all__'


class QuickJobForm(TailwindFormMixin,forms.ModelForm):
    status = forms.ModelChoiceField(queryset=TaskStatus.objects.all())
    class Meta:
        model = QuickJob
        fields = '__all__'



class ExpenseApprovalForm(TailwindFormMixin,forms.ModelForm):
    status = forms.ModelChoiceField(queryset=TaskStatus.objects.all())
    expense_type = forms.ModelChoiceField(queryset=ExpenseType.objects.all())
    class Meta:
        model = ExpenseApproval
        fields = '__all__'
        widgets = {
            'expense_title': forms.TextInput(attrs={'class': 'form-input'}),
            'project_name': forms.TextInput(attrs={'class': 'form-input'}),
            'expense_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input'}),
            'requested_by': forms.TextInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-textarea'}),
        }


from .models import SIMJob

class SIMJobForm(TailwindFormMixin,forms.ModelForm):
    status = forms.ModelChoiceField(queryset=TaskStatus.objects.all())
    class Meta:
        model = SIMJob
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
