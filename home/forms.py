from django import forms
from .models import Fooditem,Category
from dataclasses import field

class CreateFood(forms.ModelForm):
    class Meta:
        model = Fooditem
        fields= '__all__'

class CreateCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields= '__all__'