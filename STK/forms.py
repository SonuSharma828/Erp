from django import forms
from .models import STKUnit, STKCategory, STKStock, STKTake
from spp.mixins import TailwindFormMixin
from core.models import TransactionType
class STKUnitForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = STKUnit
        fields = '__all__'

class STKCategoryForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = STKCategory
        fields = '__all__'

class STKStockForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = STKStock
        fields = '__all__'

class STKTakeForm(TailwindFormMixin,forms.ModelForm):
    #transaction_type = forms.ModelChoiceField(queryset=TransactionType.objects.all())
    class Meta:
        model = STKTake
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Format date if editing
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')

        # Change the label of taken_by to 'Issued To'
        self.fields['taken_by'].label = 'Issued To'
