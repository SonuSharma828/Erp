from django.db import models
from employees.models import Employee
from customer.models import Customer  

class Project(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    address = models.TextField()
    client = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True,)
    contact_person_name = models.CharField(max_length=255, blank=True, null=True)
    contact_person_phone = models.CharField(max_length=15, blank=True, null=True)
    contact_person = models.ForeignKey(Customer, blank=True, null=True, related_name='contact_projects', on_delete=models.SET_NULL)
    status = models.CharField(max_length=20)
    startdate = models.DateField()
    deadline = models.DateField()
    gst_number = models.CharField(max_length=255,default='NA',blank=True, null=True)
    budget_equipment = models.DecimalField(max_digits=12, decimal_places=2,null=True, blank=True)
    budget_execution = models.DecimalField(max_digits=12, decimal_places=2,null=True, blank=True)

    @property
    def total_budget(self):
        equipment = self.budget_equipment or 0
        execution = self.budget_execution or 0
        return equipment + execution

    def __str__(self):
        return self.name

    def get_progress(self):
        return 60


class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('in_progress', 'In Progress'), ('pending', 'Pending')])
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    #user = models.CharField(max_length=255)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.project.name}'
    
