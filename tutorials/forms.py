from django import forms
from .models import *
  
class TutorialForm(forms.ModelForm):
  
    class Meta:
        model = Tutorial
        fields = ['title', 'description', 'published', 'Img']