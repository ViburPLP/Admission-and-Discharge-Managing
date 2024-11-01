from django import forms
from .models import Daily_update
from django.contrib.auth.models import User

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Daily_update
        fields = ['interim_bill', 'progress_notes', 'care_manager']

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

#****************************************************************************************

class SchemeForm(forms.Form):
    schemes_csv = forms.FileField()

class ProviderForm(forms.Form):
    providers_csv = forms.FileField()

