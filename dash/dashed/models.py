from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import magic

#********************************************************************************
# Custom file validators for the Scheme model's `policy_document` field.
# The `extension_validator` ensures that the uploaded file has one of the allowed extensions: .csv, .xlsx, .xls, or .pdf.
# The `validate_file_mimetype` function checks the MIME type of the uploaded file.

# extension_validator = FileExtensionValidator(['.csv', '.xlsx', '.xls', '.pdf'])

def validate_file_mimetype(file):
    accepted_mime_types = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        'application/vnd.ms-excel',
        'application/vnd.oasis.opendocument.spreadsheet',
        'text/csv', 
        'application/vnd.ms-excel', 
        'application/pdf',
        ]
    
    file_mimetype= magic.from_buffer(file.read(1024), mime=True)
    if file_mimetype not in accepted_mime_types:
        raise ValidationError('Invalid format. Please upload a valid Excel or PDF file.')
  
#********************************************************************************
class Member_Detail(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged')
    ]
    relationship = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    membership_number = models.CharField(max_length=100)
    payer = models.CharField(max_length=100)
    scheme = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    validity = models.CharField(max_length=100)
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    admission_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.name} - {self.membership_number} - {self.admission_status}"

class InsuranceDetail(models.Model):
    member = models.ForeignKey(Member_Detail, 
                               related_name='insurance_details', 
                               on_delete=models.CASCADE, null=True
                               )
    cover_type = models.CharField(max_length=100)
    cover_value = models.DecimalField(max_digits=10, decimal_places=2)
    cover_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cover_type} - {self.cover_value} - {self.cover_balance}"
    
class Scheme(models.Model):
    name=models.CharField(max_length=100)
    payer=models.CharField(max_length=100, null=True)
    rm=models.CharField(max_length=100, null=True)
    rm_contact=models.CharField(max_length=100, null=True)
    policy_start_date=models.DateField(null=True)
    policy_end_date=models.DateField(null=True)
    scheme_notes = models.TextField(null=True)
    service_provider= models.ManyToManyField('Provider', related_name='scheme', blank=True)    
    # policy_document=models.FileField(
    #     upload_to='policy_documents/', 
    #     null=True, 
    #     validators=[extension_validator, validate_file_mimetype])

    def __str__(self):
        return self.name
    
class Provider(models.Model):
    name= models.CharField(max_length=100)
    schemes= models.ManyToManyField(Scheme, related_name='providers')
    location= models.CharField(max_length=100, null=True)
    care_manager=models.CharField(max_length=100, null=True)
    cm_contact=models.CharField(max_length=100, null=True)
    services= models.CharField(max_length=100, null=True)
    provider_notes = models.TextField(null=True)
    agreed_packages= models.FileField(
        upload_to='agreed_packages/', 
        null=True, 
        validators=[validate_file_mimetype])

    def __str__(self):
        return self.name
    
class Admission_details(models.Model):
    member = models.ForeignKey(
        Member_Detail, 
        related_name='admission_details', 
        on_delete=models.CASCADE, 
        null=True)
    
    Provider = models.ForeignKey(
        Provider, 
        related_name='admission_details', 
        on_delete=models.CASCADE, null=True)
    
    admission_date = models.DateField()
    admission_diagnosis = models.CharField(max_length=100)
    cover_used = models.CharField(max_length=100)
    initial_cover_value = models.CharField(max_length=100)
    initial_cover_balance = models.CharField(max_length=100)
    requested_amount = models.CharField(max_length=100)
    lou_issued = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    admited_by = models.CharField(max_length=100)
    def save (self, *args, **kwargs):
        if not self.admited_by:
            self.admited_by = self.user.username if self.user else 'Unknown'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member.name} - {self.admission_date}"
    
class Discharge_details(models.Model):
  
    #Member_Detail
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)
    membership_number = models.CharField(max_length=100)
    payer = models.CharField(max_length=100)
    scheme = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    validity = models.CharField(max_length=100)

    #Admission_details
    admission_date = models.DateField()
    provider = models.CharField(max_length=100, null=True)
    admission_diagnosis = models.CharField(max_length=100)
    cover_used = models.CharField(max_length=100)
    initial_cover_value = models.CharField(max_length=100)
    initial_cover_balance = models.CharField(max_length=100)
    requested_amount = models.CharField(max_length=100)
    lou_issued = models.CharField(max_length=100)
    admitted_by = models.CharField(max_length=100)
        
    #added Fields
    discharge_date = models.DateField(default=timezone.now)
    final_approved_amount = models.CharField(max_length=100)
    days_admitted = models.PositiveIntegerField(default=0, null=True)
    discharge_notes = models.TextField()
    discharged_by = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        #days admitted
        if isinstance(self.discharge_date, str):
            self.discharge_date = datetime.strptime(self.discharge_date, '%Y-%m-%d').date()

        if isinstance(self.admission_date, str):
            self.admission_date = datetime.strptime(self.admission_date, '%Y-%m-%d').date()

        delta = self.discharge_date - self.admission_date
        self.days_admitted = delta.days

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.discharge_date} - Discharged"
    
class Daily_update(models.Model):
    admission = models.ForeignKey('Admission_details', on_delete=models.CASCADE, related_name='updates')
    date = models.DateTimeField(default=timezone.now)
    progress_notes = models.TextField()
    interim_bill = models.DecimalField(max_digits=100, decimal_places=2)
    care_manager = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Update on {self.date} - Interim Bill: {self.interim_bill}"
    
 
    