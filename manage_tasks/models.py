from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from employees.models import Employee  
from projects.models import Project    
from task_group.models import TaskGroup  
from dashboard.models import CustomUser
from customer.models import Customer
from core.models import PaymentMode,TaskStatus

class ServiceCharge(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Servicer Changer"
    charge = models.DecimalField(max_digits=10, decimal_places=2)  # ₹300
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=18.0)

    def total_with_tax(self):
        return round(self.charge + (self.charge * self.tax_percent / 100), 2)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('rejected', 'Rejected'),
    ]
    sno = models.AutoField(primary_key=True)
    priority = models.CharField(max_length=50)
    task_detail = models.TextField()
    date = models.DateField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=80,default='pending')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceCharge, on_delete=models.CASCADE,null=True, blank=True)

    def get_absolute_url(self):
        return reverse('edit_task', kwargs={'id':self.sno})

    def __str__(self):
        return f"{self.task_detail[:50]}..."


class TaskServiceCharge(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='service_charges')
    service = models.ForeignKey(ServiceCharge, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_with_tax(self):
        base = self.service.charge * self.quntity
        return round(base + (base * self.service.tax_percent / 100), 2)

    def __str__(self):
        return f"{self.task} - {self.service.name}"




class TaskBilling(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='billing')
    technician = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
    tools_total = models.DecimalField(max_digits=10, decimal_places=2)
    service_total = models.DecimalField(max_digits=10, decimal_places=2)
    #tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=18.0)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.PROTECT)
    final_total = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    '''
    def calculate_final(self):
        tax_amount = (self.tools_total + self.service_total) * (self.tax_percent / 100)
        return round(self.tools_total + self.service_total + tax_amount, 2)
    '''
    def __str__(self):
        return f"Bill for Task #{self.task.sno}"



class ManualItem(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='manual_items')
    item_name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()

    def get_total(self):
        return self.quantity * self.price


class ExternalExpense(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='expenses')
    item_name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()

    def get_total(self):
        return self.quantity * self.price

class CoWorkerCharge(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='coworker_charges')
    charge = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.coworker.name} - ₹{self.charge}"
