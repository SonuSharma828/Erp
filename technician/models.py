from django.db import models
from django.conf import settings

class TechnicianProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)  # optional
    feedback = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# technician/forms.py
from django import forms
from HRM.models import LeaveRequest  # assuming Leave model is in hr app

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason', 'leave_type']  # adjust to your model

