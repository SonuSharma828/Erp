# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from HRM.models import Department
from employees.models import Employee
import django.db.models.deletion
from customer.models import Customer
class CustomUser(AbstractUser):
    department = models.ForeignKey('HRM.Department',on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True)
    employee = models.OneToOneField(Employee, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        # Auto-link employee by email if not already set
        if self.email and not self.employee:
            try:
                employee = Employee.objects.get(email=self.email)
                self.employee = employee
            except Employee.DoesNotExist:
                pass  # No matching employee — skip
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return self.employee.name if self.employee else self.get_full_name()



class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=False)
    client_name = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices_created')
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.invoice_number} - {self.company.name}"

