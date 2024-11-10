from django import forms
from .models import Location  # Ensure you import your Location model

class ShortestPathForm(forms.Form):
    start = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        label="Starting Hospital",
        widget=forms.Select(attrs={'class': 'form-control'})  # Add Bootstrap class here
    )
    end = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        label="Ending Department",
        widget=forms.Select(attrs={'class': 'form-control'})  # Add Bootstrap class here
    )
