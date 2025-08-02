from django import forms
from .models import *
from core.models import ProjectStatus,ProjectType

class ProjectForm(forms.ModelForm):
    status = forms.ModelChoiceField(queryset=ProjectStatus.objects.all(),widget=forms.Select(attrs={'class': 'w-full mt-2 px-4 py-2 border rounded-md'}))
    name = forms.ModelChoiceField(queryset=ProjectType.objects.all(),widget=forms.Select(attrs={'class': 'w-full mt-2 px-4 py-2 border rounded-md'}))
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'status']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
