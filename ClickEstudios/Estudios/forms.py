from django import forms
from . import models

class Service(forms.ModelForm):
      class Meta:
            model = models.Service
            fields = ['name', 'description',  'img', 'is_active']
            widgets = {
                  'name': forms.TextInput(attrs={'class': 'form-control'}),
                  'description': forms.Textarea(attrs={'class': 'form-control'}),
                  'img': forms.FileInput(attrs={'class': 'form-control'}),
                  'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})

            }


class Plan(forms.ModelForm):
      class Meta:
            model = models.Plan
            fields = ['service', 'name', 'description', 'price', 'img', 'img_back', 'is_active']
            widgets = {
                  'service': forms.Select(attrs={'class': 'form-control'}),
                  'name': forms.TextInput(attrs={'class': 'form-control'}),
                  'description': forms.Textarea(attrs={'class': 'form-control'}),
                  'price': forms.NumberInput(attrs={'class': 'form-control'}),
                  'img': forms.FileInput(attrs={'class': 'form-control'}),
                  'img_back': forms.FileInput(attrs={'class': 'form-control'}),
                  'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
            }