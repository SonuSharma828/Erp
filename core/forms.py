from django import forms
from .models import (
    TaskImportance, ProjectStatus, TaskStatus, TransactionType,
    Segment, PaymentMode, EntryType, ExpenseType, VoucherType,
    EmployeePaymentType, LeaveType,SppTransactionType,AttendanceStatusType,KnwGroupType,KnwSubGroupType,ProjectType,PhotoIdType,Company, AmountType
)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

class AmountTypeForm(forms.ModelForm):
    class Meta:
        model = AmountType
        fields = ['name']

class TaskImportanceForm(forms.ModelForm):
    class Meta:
        model = TaskImportance
        fields = ['name']

class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model = ProjectStatus
        fields = ['name']

class ProjectTypeForm(forms.ModelForm):
    class Meta:
        model = ProjectType
        fields = ['name']

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = TaskStatus
        fields = ['name']

class PhotoIdTypeForm(forms.ModelForm):
    class Meta:
        model = PhotoIdType
        fields = ['name']

class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = ['name']

class SegmentForm(forms.ModelForm):
    class Meta:
        model = Segment
        fields = ['name']

class PaymentModeForm(forms.ModelForm):
    class Meta:
        model = PaymentMode
        fields = ['name']

class EntryTypeForm(forms.ModelForm):
    class Meta:
        model = EntryType
        fields = ['name']

class ExpenseTypeForm(forms.ModelForm):
    class Meta:
        model = ExpenseType
        fields = ['name']

class VoucherTypeForm(forms.ModelForm):
    class Meta:
        model = VoucherType
        fields = ['name']

class EmployeePaymentTypeForm(forms.ModelForm):
    class Meta:
        model = EmployeePaymentType
        fields = ['name']

class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['name']

class SppTransactionTypeForm(forms.ModelForm):
    class Meta:
        model = SppTransactionType
        fields = ['name']


class AttendanceStatusTypeForm(forms.ModelForm):
    class Meta:
        model = AttendanceStatusType
        fields = ['name']



class KnwGroupTypeForm(forms.ModelForm):
    class Meta:
        model = KnwGroupType
        fields = ['name']


class KnwSubGroupTypeForm(forms.ModelForm):
    class Meta:
        model = KnwSubGroupType
        fields = ['name']
