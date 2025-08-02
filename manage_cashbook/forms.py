from django import forms
from .models import CashbookEntry
from .mixins import TailwindFormMixin
from core.models import PaymentMode,Segment,EntryType

class CashbookEntryForm(TailwindFormMixin,forms.ModelForm):
    payment_mode = forms.ModelChoiceField(queryset=PaymentMode.objects.all())
    segment = forms.ModelChoiceField(queryset=Segment.objects.all())
    entry_type = forms.ModelChoiceField(queryset=EntryType.objects.all())
    class Meta:
        model = CashbookEntry
        fields = '__all__'
        exclude = ['created_by', 'created_at']
        widgets = {
            'entry_date': forms.DateInput(attrs={'type': 'date'}),
        }
