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


from .models import Provider, Scheme
from django import forms


# class SchemeAdminForm(forms.ModelForm):
#     class Meta:
#         model = Scheme
#         fields = [ 
#             'service_provider'
#         ]
        
#     service_provider = forms.ModelMultipleChoiceField(
#         queryset=Provider.objects.all(),
#         widget=forms.SelectMultiple(attrs={'class': 'dual_select'}),
#         required=False
#     )

# class SchemeAdd (forms.ModelForm):
#     class Meta:
#         model = Scheme
#         fields = '__all__'
class SchemeAdminForm(forms.ModelForm):
    providers = forms.ModelMultipleChoiceField(
        queryset=Provider.objects.all(), 
        widget=forms.SelectMultiple(attrs={'class': 'dual_select'}), 
        required=False
    )

    class Meta:
        model = Scheme
        exclude = ['name', 'payer', 'rm', 'rm_contact', 'policy_start_date', 'policy_end_date', 'scheme_notes'] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  
            self.fields['providers'].initial = self.instance.providers.all()

    def save(self, commit=True):
        scheme = super().save(commit=False)  
        if commit:
            scheme.save()
            self.instance.providers.set(self.cleaned_data['providers']) #updating m2m relationship
        return scheme


class SchemeAddForm(forms.ModelForm):
    class Meta:
        model = Scheme
        fields = '__all__'


