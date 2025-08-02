from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
from django.conf import settings
#from dashboard.models import CustomUser
from core.models import TaskStatus


class Department(models.Model):
    sno = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='created_departments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name


class Empdata(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    email = models.EmailField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    in_payroll = models.BooleanField(default=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.name}"

    
# HRM/models.py

from .models import Department  
from employees.models import Employee
from core.models import PaymentMode,EmployeePaymentType


class EmployeePayment(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    payment_method = models.ForeignKey(PaymentMode, on_delete=models.PROTECT)
    type = models.ForeignKey(EmployeePaymentType, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved = models.BooleanField(default=False)
    location = models.CharField(max_length=100)

    approval_status = models.ForeignKey(TaskStatus, on_delete=models.PROTECT, related_name='employee_payments')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_employee_payments')
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.type.name} - {self.amount}"



from django.db import models
from django.conf import settings

LEAVE_TYPE_CHOICES = [
    ('sick', 'Sick Leave'),
    ('casual', 'Casual Leave'),
    ('earned', 'Earned Leave'),
]

LEAVE_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class LeaveRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewer_remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.status})"
