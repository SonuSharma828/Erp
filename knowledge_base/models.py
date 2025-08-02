from django.db import models
from HRM.models import Department

class KnowledgeBase(models.Model):
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    group = models.CharField(max_length=100)
    subgroup = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    descriptions = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
