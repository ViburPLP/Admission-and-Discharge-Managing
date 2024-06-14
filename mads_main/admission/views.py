from django.shortcuts import render
from .models import MemberDetail, InsuranceDetail

def pending_admissions(request):
    members = MemberDetail.objects.all()
    return render(request, 'admission/pending_admissions.html', {'members': members})

def admit_patient(request, membership_number):
    member = MemberDetail.objects.get(membership_number=membership_number)
    insurance_details = InsuranceDetail.objects.filter(membership_number=member)
    return render(request, 'admission/admit_patient.html', {'member': member, 'insurance_details': insurance_details})

# Create your views here.
