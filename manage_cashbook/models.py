from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from core.models import PaymentMode,Segment,EntryType

class CashbookEntry(models.Model):
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.DO_NOTHING)
    segment = models.ForeignKey(Segment,on_delete=models.DO_NOTHING)
    entry_date = models.DateField()
    entry_type = models.CharField(max_length=80,null=True , blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.entry_type} - {self.amount} on {self.entry_date}"
