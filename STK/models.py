from django.db import models
from dashboard.models import CustomUser
from core.models import TransactionType
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# STK Units
class STKUnit(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

# STK Categories
class STKCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# STK (Stock Items)
class STKStock(models.Model):
    item_name = models.CharField(max_length=150)
    category = models.ForeignKey(STKCategory, on_delete=models.CASCADE)
    unit = models.ForeignKey(STKUnit, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

# STK Take (Stock Transactions)
class STKTake(models.Model):
    TRANSACTION_TYPE = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )

    item = models.ForeignKey(STKStock, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    taken_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    '''
    _original_quantity = None
    _original_type = None
    '''

    def __str__(self):
        return f"{self.transaction_type} - {self.item.item_name}"
# 🧨 Fix delete logic
@receiver(pre_delete, sender=STKTake)
def reverse_stock_on_delete(sender, instance, **kwargs):
    if instance.transaction_type == 'IN':
        instance.item.quantity -= instance.quantity
    elif instance.transaction_type == 'OUT':
        instance.item.quantity += instance.quantity
    instance.item.save()
# models.py
class STKStockHistory(models.Model):
    item = models.ForeignKey(STKStock, on_delete=models.CASCADE, related_name='histories')
    quantity_added = models.DecimalField(max_digits=10, decimal_places=2)
    price_at_time = models.DecimalField(max_digits=12, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.CharField(max_length=100, default='System')

    def __str__(self):
        return f"{self.item.item_name} - {self.quantity_added} @ ₹{self.price_at_time} on {self.added_at.date()}"

