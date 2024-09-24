from django.forms import ModelForm
from . models import approvals

class UIModelForm(ModelForm):
	class Meta:
		model=approvals
		fields = '__all__'
		#exclude = 'firstname'


# forms.py
from django import forms
from .models import FertilizerRecommendation

class FertilizerForm(forms.ModelForm):
    CROP_TYPE_CHOICES = [
        ('maize', 'Maize'),
        ('rice', 'Rice'),
        ('wheat', 'Wheat'),
    ]
    SOIL_TYPE_CHOICES = [
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loam', 'Loam'),
    ]
    crop_type = forms.ChoiceField(choices=CROP_TYPE_CHOICES)
    soil_type = forms.ChoiceField(choices=SOIL_TYPE_CHOICES)
    nitrogen_level = forms.IntegerField()
    phosphorus_level = forms.IntegerField()
    potassium_level = forms.IntegerField()
    
    class Meta:
        model = FertilizerRecommendation
        fields = ['crop_type', 'soil_type', 'nitrogen_level', 'phosphorus_level', 'potassium_level']
