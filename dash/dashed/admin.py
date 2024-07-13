from django.contrib import admin
from .models import MemberDetail, Discharge, Discharged, Member_Detail, InsuranceDetail

# admin.site.register(Person)
admin.site.register(MemberDetail)
admin.site.register(Member_Detail)
admin.site.register(Discharge)
admin.site.register(Discharged)
admin.site.register(InsuranceDetail)

# Register your models here.
