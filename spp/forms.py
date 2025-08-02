from django import forms
from .models import SparePartTransaction
from .models import Voucher
from .mixins import TailwindFormMixin
from core.models import PaymentMode,ExpenseType,SppTransactionType,VoucherType,AmountType
from .models import MonthlySale, MonthlyExpense, MonthlyVendorPayment

class SparePartTransactionForm(TailwindFormMixin,forms.ModelForm):
    payment_mode = forms.ModelChoiceField(queryset=PaymentMode.objects.all())
    transaction_type = forms.ModelChoiceField(queryset=SppTransactionType.objects.all())
    class Meta:
        model = SparePartTransaction
        fields = ['sparepart', 'transaction_type', 'quantity', 'amount', 'payment_mode', 'transaction_date']
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
        }




class VoucherForm(TailwindFormMixin,forms.ModelForm):
    payment_mode = forms.ModelChoiceField(queryset=PaymentMode.objects.all())
    voucher_type = forms.ModelChoiceField(queryset=VoucherType.objects.all())
    class Meta:
        model = Voucher
        fields = '__all__'
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
        }


'''
from .models import MonthlySale, MonthlyExpense, MonthlyVendorPayment

class MonthlySaleForm(TailwindFormMixin,forms.ModelForm):
    payment_mode = forms.ModelChoiceField(queryset=PaymentMode.objects.all())
    class Meta:
        model = MonthlySale
        fields = ['date', 'amount', 'payment_mode', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
'''

from django import forms
from .models import MonthlySale, PaymentEntry
from django.forms.models import inlineformset_factory

class MonthlySaleForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = MonthlySale
        fields = ['company','invoice_number', 'date', 'product', 'amount', 'description']

class PaymentEntryForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = PaymentEntry
        fields = ['payment_type', 'amount']
        widgets = {
            'payment_type': forms.Select(attrs={'class': 'border text-red-600'}),
        }

PaymentEntryFormSet = inlineformset_factory(
    MonthlySale,
    PaymentEntry,
    form=PaymentEntryForm,
    extra=4,
    can_delete=True
)

class MonthlyExpenseForm(TailwindFormMixin,forms.ModelForm):
    expense_type = forms.ModelChoiceField(queryset=ExpenseType.objects.all())
    amount_type = forms.ModelChoiceField(queryset=AmountType.objects.all())
    class Meta:
        model = MonthlyExpense
        exclude = ['total_expenses']
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class MonthlyVendorPaymentForm(TailwindFormMixin,forms.ModelForm):
    #payment_mode = forms.ModelChoiceField(queryset=PaymentMode.objects.all())
    class Meta:
        model = MonthlyVendorPayment
        fields = ['vendor_name', 'date', 'amount', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
