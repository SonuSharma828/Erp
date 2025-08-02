from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

def validate_file_size(file):
    max_size_mb = 2
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size should not exceed {max_size_mb}MB.")

PHOTO_ID_CHOICES = [
    ('aadhaar', 'Aadhaar Card'),
    ('pan', 'PAN Card'),
    ('voter', 'Voter ID'),
    ('passport', 'Passport'),
    ('license', 'Driving License'),
]

class Employee(models.Model):
    sno = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,related_name='employee_profile')
    position = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=35,null=True, blank=True)
    address = models.TextField()
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='employee_photos/',validators=[validate_file_size], null=True, blank=True,default='employee_photos/user.png')

    # 🔽 New fields
    photo_id_type = models.CharField(max_length=20, null=True, blank=True)
    photo_id_file = models.FileField(upload_to='employee_id_docs/', validators=[validate_file_size], null=True, blank=True)

    def __str__(self):
        return self.name

