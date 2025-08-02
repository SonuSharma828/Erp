from django import forms
from .models import Customer,ContactPerson
from .mixins import TailwindFormMixin

class CustomerForm(TailwindFormMixin,forms.ModelForm):
    contact_data = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Customer
        fields = '__all__'

class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ['name', 'phone']
