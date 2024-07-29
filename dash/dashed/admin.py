from django.contrib import admin
from .models import (
    MemberDetail, 
    Discharge, 
    Discharged, 
    Member_Detail, 
    InsuranceDetail, 
    Scheme, 
    Provider,
    Admission_details
    )

class ProviderInline(admin.TabularInline):
    model = Provider.schemes.through  # Specify the through model
    extra = 1  # Number of extra empty forms to display

class SchemeAdmin(admin.ModelAdmin):
    inlines = [ProviderInline]

class ProviderAdmin(admin.ModelAdmin):
    inlines = [ProviderInline]
    exclude = ('schemes',)  # Hide the 'schemes' field to avoid confusion


# admin.site.register(Person)
admin.site.register(MemberDetail)
admin.site.register(Member_Detail)
admin.site.register(Discharge)
admin.site.register(Discharged)
admin.site.register(InsuranceDetail)
admin.site.register(Scheme, SchemeAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Admission_details)

# Register your models here.
