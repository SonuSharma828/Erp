from django.db import models

class Supplier(models.Model):
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    supplier_name = models.CharField(max_length=200)
    address = models.TextField()
    country_code = models.CharField(max_length=5, choices=[
        ('+91', '+91'),
        ('+1', '+1'),
        ('+44', '+44'),
        ('+61', '+61'),
    ], default='+91')
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    company = models.ForeignKey('core.Company', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.supplier_name


class ContactPerson(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Bill(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='bills')
    bill_number = models.CharField(max_length=50)
    bill_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    invoice = models.FileField(upload_to='invoices/', blank=True, null=True)

    def __str__(self):
        return f"{self.bill_number} - {self.amount}"

