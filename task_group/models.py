from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings

class TaskGroup(models.Model):
    sno = models.AutoField(primary_key=True)
    task_group_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_group_name

