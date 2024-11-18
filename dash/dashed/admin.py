from django.contrib import admin
from .models import (
    Member_Detail, 
    InsuranceDetail, 
    Scheme, 
    Provider,
    Admission_details,
    Discharge_details,
    Daily_update
    )
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
import csv

from .models import Provider, Scheme
    

class ProviderInline(admin.TabularInline):
    model = Provider.schemes.through  # Specify the through model
    extra = 1  # Number of extra empty forms to display

class SchemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'payer']
    search_fields = ['name', 'payer']
    filter_horizontal = [ 'service_provider']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-schemes/', self.admin_site.admin_view(self.bulk_create_schemes), name='bulk_create_schemes'),
        ]
        return custom_urls + urls

    def bulk_create_schemes (self, request):
      if request.method == 'POST':
        if 'csv_file' in request.FILES:
          file = request.FILES['csv_file']
          csv_data = file.read().decode('utf-8'). splitlines()
          reader = csv.reader(csv_data)

          next(reader, None)

          created_count = 0
          for row in reader: 
            if len(row)>= 2:
              name = row[0]. strip()
              payer = row[1].strip()
              rm = row[2].strip()
              rm_contact = row[3].strip()
              policy_start_date = row[4].strip()
              policy_end_date = row[5].strip()

              Scheme.objects.create(name=name, payer= payer)
              created_count +=1
          self.message_user(request, f"{created_count} schemes created from csv")
          return HttpResponseRedirect('..')
      return render(request, "admin/dashed/schemes/bulk_create_schemes.html")

admin.site.register(Scheme, SchemeAdmin)

class ProviderAdmin(admin.ModelAdmin):
    inlines = [ProviderInline]
    exclude = ('schemes',)  # Hide the 'schemes' field to avoid confusion

class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    filter_horizontal = [ 'schemes']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-create/', self.admin_site.admin_view(self.bulk_create_view), name='bulk_create_providers'),
        ]
        return custom_urls + urls

    def bulk_create_view(self, request):
        if request.method == 'POST':
            if 'provider_names' in request.POST:
                # Process provider names from a textarea
                provider_names = request.POST['provider_names'].splitlines()
                created_count = 0
                for name in provider_names:
                    name = name.strip()
                    if name:
                        Provider.objects.create(name=name)
                        created_count += 1
                self.message_user(request, f"{created_count} providers created.")
                return HttpResponseRedirect("..")

            elif 'csv_file' in request.FILES:
                # Process a CSV file upload
                file = request.FILES['csv_file']
                csv_data = file.read().decode('utf-8').splitlines()
                reader = csv.reader(csv_data)

                # Skip the header if present
                next(reader, None)

                created_count = 0
                for row in reader:
                    if row:
                        provider_name = row[0].strip()
                        location = row[1].strip()
                        care_manager = row[2].strip()
                        cm_contact = row[3].strip()
                        services = row[4].strip()
                        if provider_name:
                            Provider.objects.create(name=provider_name, location=location, care_manager=care_manager, cm_contact=cm_contact, services=services)
                            created_count += 1
                self.message_user(request, f"{created_count} providers created from CSV.")
                return HttpResponseRedirect("..")

        return render(request, "admin/dashed/provider/bulk_create_providers_form.html", {'title': 'Bulk Create Providers'})


admin.site.register(Provider, ProviderAdmin)

# admin.site.register(Person)
admin.site.register(Member_Detail)
admin.site.register(InsuranceDetail)
admin.site.register(Admission_details)
admin.site.register(Discharge_details)
admin.site.register(Daily_update)

# Register your models here.
