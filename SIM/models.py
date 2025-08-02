from django.db import models
#from django.contrib.auth.models import User
from projects.models import Project
from django.conf import settings
from customer.models import Customer

class DailyStatus(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    last_transaction = models.PositiveIntegerField()
    current_transaction = models.PositiveIntegerField()
    updated = models.DateField(auto_now=True)
    managed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.project.name} - {self.updated}"

# sim/models.py

class PaymentFollowUp(models.Model):
    job_completed = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, blank=True)
    address = models.TextField()
    job = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.customer.customer_name} - {self.job_completed.name}"
    



class QuickJob(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    project_name = models.CharField(max_length=255)
    job_type = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.project_name} - {self.customer_name}"
    


class ExpenseApproval(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('Material', 'Material'),
        ('Labour', 'Labour'),
        ('Travel', 'Travel'),
        ('Misc', 'Misc'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    expense_title = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    expense_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateField(auto_now_add=True)
    requested_by = models.CharField(max_length=100)
    status = models.CharField(max_length=80,default='Pending')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.expense_title} - {self.project_name}"
    


class SIMJob(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    project_name = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    address = models.TextField()
    job_description = models.TextField()
    status = models.CharField(max_length=80,default='Pending')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.project_name} - {self.customer_name} - {self.status}"

