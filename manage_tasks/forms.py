from django import forms
from .models import *
from .mixins import TailwindFormMixin
from core.models import TaskImportance,TaskStatus
from employees.models import Employee
from customer.models import Customer

class TaskForm(TailwindFormMixin,forms.ModelForm):
    priority = forms.ModelChoiceField(queryset=TaskImportance.objects.all())
    #status = forms.ModelChoiceField(queryset=TaskStatus.objects.all())
    class Meta:
        model = Task
        exclude = ['status']
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'task_detail': forms.Textarea(attrs={'rows': 3}),
        }




from django import forms
from .models import ServiceCharge

class ServiceChargeForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = ServiceCharge
        fields = ['name', 'charge', 'tax_percent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'charge': forms.NumberInput(attrs={'class': 'input'}),
            'tax_percent': forms.NumberInput(attrs={'class': 'input'}),
        }
