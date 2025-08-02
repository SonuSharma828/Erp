from django import forms
from django.contrib.auth.forms import UserCreationForm
from SIM.mixins import TailwindFormMixin
from .models import CustomUser
from employees.models import Employee  # make sure you import it
'''
class AdminCreateUserForm(TailwindFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'department', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)

        # Try to find matching employee by email
        employees = Employee.objects.filter(email=user.email)
        if employees.exists():
           employee = employees.first()  # take the first one
           user.first_name = employee.name  # optional: store name as first_name
           user.employee = employee        # Optional if FK exists
        else:
           pass  # no employee found

        if commit:
           user.save()
        return user
'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from SIM.mixins import TailwindFormMixin
from .models import CustomUser
from employees.models import Employee

class AdminCreateUserForm(TailwindFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'department', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = CustomUser.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        # Link to employee by email
        employees = Employee.objects.filter(email=user.email)
        if employees.exists():
            employee = employees.first()
            user.first_name = employee.name
            user.employee = employee  # if CustomUser has FK to Employee
        else:
            pass  # no employee found

        if commit:
            user.save()
        return user


# forms.py

from django import forms
from .models import Company, Invoice

class CompanyForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'gst_number', 'address']

class InvoiceForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['company', 'invoice_number', 'client_name', 'amount']

