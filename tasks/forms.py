from django import forms
from django.forms import ModelForm
from .models import task
class task_form(ModelForm):
    class Meta:
        model = task
        fields = ['title', 'description', 'is_important']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a title'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Write a description'}),
            'is_important':forms.CheckboxInput(attrs={'class':'form-check-input'})
        }

