from django.db import models
from django.utils import timezone
from core.models import PaymentMode
from dashboard.models import Company
from supplier.models import Supplier
from collections import defaultdict

# Spare Part Record
class SparePart(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Spare Part Transactions
class SparePartTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('New Record', 'New Record'),
        ('Sales', 'Sales'),
        ('Expense', 'Expense'),
        ('Supplier Payment', 'Supplier Payment'),
        ('Transfer', 'Transfer'),
        ('C/F Balance Entry', 'C/F Balance Entry'),
    ]
   
    sparepart = models.ForeignKey(SparePart, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=100)
    quantity = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20, null=True, blank=True)
    remarks = models.TextField(blank=True)
    transaction_date = models.DateField()

    def __str__(self):
        return f"{self.transaction_type} - {self.sparepart.name}"



class Voucher(models.Model):
    VOUCHER_TYPES = [
        ('sales', 'Sales'),
        ('expense', 'Expense'),
        ('supplier_payment', 'Supplier Payment'),
    ]

    voucher_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    description = models.TextField()
    payment_mode = models.CharField(max_length=80)
    
    def __str__(self):
        return f"{self.voucher_type} - {self.amount} on {self.transaction_date}"

from django.db import models
from STK.models import STKStock

class MonthlySale(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True, blank=True)
    invoice_number = models.CharField(max_length=100, null=True, blank=True, unique=False)
    date = models.DateField(default=timezone.now)
    product = models.ForeignKey(STKStock, on_delete=models.CASCADE,null=True, blank=True)
    amount = models.DecimalField(max_digits=80, decimal_places=2)
    description = models.TextField()
    total_sales = models.DecimalField(max_digits=120, decimal_places=2, default=0)

    def __str__(self):
        return f"Invoice #{self.invoice_number} - Sale on {self.date}"

    def payment_difference_abs(self):
        return abs(self.amount - self.total_payment())

    def payment_difference(self):
        return self.total_payment() - self.amount

    def total_payment(self):
        return sum(p.amount for p in self.payments.all())

    def payment_status_color(self):
        diff = self.payment_difference()
        if diff == 0:
            return 'text-green-600'
        elif diff < 0:
            return 'text-red-600'
        else:
            return 'text-yellow-600'

    def payment_message(self):
        diff = self.payment_difference()
        if diff < 0:
            return f"Pending ₹{abs(diff)}"
        elif diff > 0:
            return f"Overpaid ₹{abs(diff)}"
        return "Settled"

class PaymentEntry(models.Model):
    sale = models.ForeignKey(MonthlySale, related_name='payments', on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=80, choices=[
        ('gpay', 'GPay'),
        ('paytm', 'Paytm'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('cash', 'Cash')
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.payment_type} - ₹{self.amount}"

from employees.models import Employee
from django.db import models

class MonthlyExpense(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_type = models.CharField(max_length=100)
    expense_type = models.CharField(max_length=100)
    description = models.TextField()
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.employee:
            # create a deduction record (see below)
            SalaryDeduction.objects.create(
                employee=self.employee,
                expense=self,
                amount=self.amount,
                description=self.description
            )

    def __str__(self):
        return f"Expense on {self.date}: ₹ {self.amount}"


class SalaryDeduction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    expense = models.ForeignKey(MonthlyExpense, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Deduction: ₹{self.amount} for {self.employee}"



class MonthlyVendorPayment(models.Model):
    vendor_name = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # expected total payment
    description = models.TextField()
    #total_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
   

    def __str__(self):
        return f"Payment to {self.vendor_name} on {self.date}: ₹{self.amount}"
    
    @property
    def total_payments(self):
        return sum(p.amount for p in self.payments.all())

    def total_payment(self):
        return sum(p.amount for p in self.payments.all())

    def payment_difference(self):
        return self.total_payment() - self.amount

    def payment_status_color(self):
        diff = self.payment_difference()
        if diff == 0:
            return 'text-green-600'
        elif diff < 0:
            return 'text-red-600'
        return 'text-yellow-600'

    def payment_message(self):
        diff = self.payment_difference()
        if diff < 0:
            return f"Pending ₹{abs(diff)}"
        elif diff > 0:
            return f"Overpaid ₹{abs(diff)}"
        return "Settled"

    def pending_amount(self):
        return max(0, self.amount - self.total_payments)

    def payment_summary(self):
        # Group amounts by payment_type name
        grouped = defaultdict(float)
        for entry in self.payments.all():
            grouped[entry.payment_type.name] += float(entry.amount)

            # Build summary string with grouped totals
        return ", ".join([f"{ptype}: ₹{amount:.2f}" for ptype, amount in grouped.items()])



class VendorPaymentEntry(models.Model):
    vendor_payment = models.ForeignKey(MonthlyVendorPayment, related_name='payments', on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentMode, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.payment_type} - ₹{self.amount}"

