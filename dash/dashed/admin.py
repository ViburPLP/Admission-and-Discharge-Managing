from django.contrib import admin
from .models import MemberDetail, Discharge, Discharged

# admin.site.register(Person)
admin.site.register(MemberDetail)
admin.site.register(Discharge)
admin.site.register(Discharged)

# Register your models here.
