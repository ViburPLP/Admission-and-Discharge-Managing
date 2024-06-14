from django.db import models
from django.contrib.auth.models import User

class Facility(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class MemberDetail(models.Model):
    payer = models.CharField(max_length=255)
    membership_number = models.CharField(max_length=255, unique=True)
    relationship = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    validity = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    scheme = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class InsuranceDetail(models.Model):
    membership_number = models.ForeignKey(MemberDetail, on_delete=models.CASCADE)
    cover_type = models.CharField(max_length=255)
    cover_value = models.CharField(max_length=255)
    cover_balance = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.cover_type} - {self.cover_value}"    


class Admission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
    ]

    patient = models.ForeignKey(MemberDetail, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=255)
    tentative_expense = models.DecimalField(max_digits=10, decimal_places=2)
    admission_date = models.DateField()
    discharge_date = models.DateField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending' )

    def __str__(self):
        return f" Admission for {self.patient} at {self.facility}"
    
class InterimBill(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interim Bill for {self.patient} at {self.Facility}"
    
    
    


# Create your models here.


