from django.db import models

class Income(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('UPI', 'UPI'),
        ('Cheque', 'Cheque'),
        ('Other', 'Other'),
    ]

    SOURCE_CHOICES = [
        ('Sale', 'Sale'),
        ('Service', 'Service'),
        ('Donation', 'Donation'),
        ('Other', 'Other'),
    ]

    date = models.DateField()
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.source} - ₹{self.amount} on {self.date}"


class Expense(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('UPI', 'UPI'),
        ('Cheque', 'Cheque'),
        ('Other', 'Other'),
    ]

    CATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Bills', 'Bills'),
        ('Office Supplies', 'Office Supplies'),
        ('Salaries', 'Salaries'),
        ('Transport', 'Transport'),
        ('Other', 'Other'),
    ]

    date = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} - ₹{self.amount} on {self.date}"

class SalaryPayment(models.Model):
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=[
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('UPI', 'UPI'),
        ('Cheque', 'Cheque'),
    ])
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Salary Payment to {self.employee} - ₹{self.salary_amount} on {self.payment_date}"
