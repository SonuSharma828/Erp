from django import forms
from .models import *

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'source', 'amount', 'payment_method', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'payment_method', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        }

class SalaryPaymentForm(forms.ModelForm):
    class Meta:
        model = SalaryPayment
        
        fields = ['employee', 'salary_amount', 'payment_date', 'payment_method', 'notes']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        }