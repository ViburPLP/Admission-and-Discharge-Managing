from django import forms
from .models import Daily_update

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Daily_update
        fields = ['progress_notes', 'interim_bill', 'care_manager']
