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

@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'payer']
    filter_horizontal = [ 'service_provider']

    class Media:
        js = ('scheme_admin.js',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if form.cleaned_data.get('provider_panels'):
            selected_providers = Provider.objects.filter(
                panels__in=form.cleaned_data['provider_panels']
            ).distinct()
            obj.providers.add(*selected_providers)

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

              Scheme.objects.create(name=name, payer= payer)
              created_count +=1
          self.message_user(request, f"{created_count} schemes created from csv")
          return HttpResponseRedirect('..')
      return render(request, "admin/dashed/schemes/bulk_create_schemes.html")

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
                        if provider_name:
                            Provider.objects.create(name=provider_name)
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
