from django import forms
from .models import Supplier,Bill,ContactPerson
from .mixins import TailwindFormMixin

class SupplierForm(TailwindFormMixin,forms.ModelForm):
    contact_data = forms.CharField(widget=forms.HiddenInput(), required=False)
    bill_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Supplier
        fields = ['supplier_name', 'gst_number', 'address', 'company', 'country_code', 'phone', 'email']
class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['bill_number', 'bill_date', 'amount', 'description', 'invoice']
class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ['name', 'phone']
