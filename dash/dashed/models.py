from django.db import models

class MemberDetail(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    payer = models.CharField(max_length=255)
    membership_number = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)
    validity = models.CharField(max_length=255)
    scheme = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.membership_number})"

class Discharge(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    payer = models.CharField(max_length=255)
    membership_number = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)
    validity = models.CharField(max_length=255)
    scheme = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.membership_number})"

class Discharged(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    payer = models.CharField(max_length=255)
    membership_number = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)
    validity = models.CharField(max_length=255)
    scheme = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.membership_number})"
    

class Member_Detail(models.Model):
    relationship = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    membership_number = models.CharField(max_length=100)
    payer = models.CharField(max_length=100)
    scheme = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    validity = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.membership_number}"

class InsuranceDetail(models.Model):
    member = models.ForeignKey(Member_Detail, related_name='insurance_details', on_delete=models.CASCADE, null=True)
    cover_type = models.CharField(max_length=100)
    cover_value = models.DecimalField(max_digits=10, decimal_places=2)
    cover_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cover_type} - {self.cover_value} - {self.cover_balance}"
