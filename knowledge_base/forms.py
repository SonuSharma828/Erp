from django import forms
from .models import KnowledgeBase
from core.models import KnwGroupType,KnwSubGroupType
from SIM.mixins import TailwindFormMixin

class KnowledgeBaseForm(TailwindFormMixin,forms.ModelForm):
    group = forms.ModelChoiceField(queryset=KnwGroupType.objects.all())
    subgroup = forms.ModelChoiceField(queryset=KnwSubGroupType.objects.all())
    class Meta:
        model = KnowledgeBase
        fields = '__all__'
        widgets = {
            'department': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
            'group': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
            'subgroup': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
            'name': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
            'description':forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
        }
