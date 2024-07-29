from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.utils.dateparse import parse_date
from .models import (
    Discharge, 
    MemberDetail, 
    Discharged, 
    Member_Detail, 
    InsuranceDetail,
    Scheme,
    Provider,
    Admission_details
    )




@login_required
def index(request):
    members = MemberDetail.objects.all()
    return render(request, 'index.html', {'members': members})

@login_required
def member_detail(request, pk):
    member = get_object_or_404(MemberDetail, pk=pk)
    return render(request, 'member_detail.html', {'member': member})


def admit_member(request, pk):
    admission = MemberDetail.objects.get(pk=pk)
    discharge = Discharge.objects.create(
        first_name=admission.first_name,
        last_name=admission.last_name,
        payer=admission.payer,
        membership_number=admission.membership_number,
        relationship=admission.relationship,
        validity=admission.validity,
        scheme=admission.scheme,
    )
    admission.delete()
    return redirect("discharge_member_detail", pk=discharge.pk)


@login_required
def discharge_list(request):
    discharges = Discharge.objects.all()
    return render(request, 'discharge.html', {'discharges': discharges})

@login_required
def discharge_member_detail(request, pk):
    discharge_member = get_object_or_404(Discharge, pk=pk)
    return render(request, 'Discharge_member.html', {'member': discharge_member})

def discharge_member(request, pk):
    discharges = Discharge.objects.get(pk=pk)
    discharged = Discharged.objects.create(
        first_name=discharges.first_name,
        last_name=discharges.last_name,
        payer=discharges.payer,
        membership_number=discharges.membership_number,
        relationship=discharges.relationship,
        validity=discharges.validity,
        scheme=discharges.scheme,
    )
    discharges.delete()
    return redirect("discharge_list")

def undo_admit_member(request, pk):
    discharge = get_object_or_404(Discharge, pk=pk)
    MemberDetail.objects.create(
        first_name=discharge.first_name,
        last_name=discharge.last_name,
        payer=discharge.payer,
        membership_number=discharge.membership_number,
        relationship=discharge.relationship,
        validity=discharge.validity,
        scheme=discharge.scheme,
    )
    discharge.delete()
    return redirect('index')

def undo_discharge_member(request, pk):
    discharged = get_object_or_404(Discharged, pk=pk)
    Discharge.objects.create(
        first_name=discharged.first_name,
        last_name=discharged.last_name,
        payer=discharged.payer,
        membership_number=discharged.membership_number,
        relationship=discharged.relationship,
        validity=discharged.validity,
        scheme=discharged.scheme,
    )
    discharged.delete()
    return redirect('discharge_list')

@login_required
def discharged_list(request):
    discharged_member = Discharged.objects.all()
    return render(request, 'Discharged_list.html', {'discharged_member': discharged_member})

@login_required
def discharged_member_detail(request, pk):
    discharged_member = get_object_or_404(Discharged, pk=pk)
    return render(request, 'discharged_member.html', {'member': discharged_member})


@login_required
def index(request):
    query = request.GET.get('q')
    payer_filter = request.GET.get('payer')
    scheme_filter = request.GET.get('scheme')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    order = request.GET.get('order', 'added_at')

    members = MemberDetail.objects.all()

    if query:
        members = members.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(membership_number__icontains=query)
        )
    if payer_filter:
        members = members.filter(payer__icontains=payer_filter)
    if scheme_filter:
        members = members.filter(scheme__icontains=scheme_filter)
    if date_from:
        members = members.filter(added_at__gte=parse_date(date_from))
    if date_to:
        members = members.filter(added_at__lte=parse_date(date_to))

    members = members.order_by(order)
    
    return render(request, 'index.html', {'members': members, 'query': query, 'payer_filter': payer_filter, 'scheme_filter': scheme_filter, 'date_from': date_from, 'date_to': date_to, 'order': order})


@login_required
def discharge_list(request):
    query = request.GET.get('q')
    payer_filter = request.GET.get('payer')
    scheme_filter = request.GET.get('scheme')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    order = request.GET.get('order', 'added_at')

    discharges = Discharge.objects.all()

    if query:
        discharges = discharges.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(membership_number__icontains=query) |
            Q(payer__icontains=query) |
            Q(relationship__icontains=query) |
            Q(validity__icontains=query) |
            Q(scheme__icontains=query)
        )
    if payer_filter:
        discharges = discharges.filter(payer__icontains=payer_filter)
    if scheme_filter:
        discharges = discharges.filter(scheme__icontains=scheme_filter)
    if date_from:
        discharges = discharges.filter(added_at__gte=parse_date(date_from))
    if date_to:
        discharges = discharges.filter(added_at__lte=parse_date(date_to))

    discharges = discharges.order_by(order)

    return render(request, 'discharge.html', {'discharges': discharges, 'query': query, 'payer_filter': payer_filter, 'scheme_filter': scheme_filter, 'date_from': date_from, 'date_to': date_to, 'order': order})

@login_required
def discharged_list(request):
    query = request.GET.get('q')
    if query:
        discharged_member = Discharged.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(payer__icontains=query) |
            Q(membership_number__icontains=query) |
            Q(relationship__icontains=query) |
            Q(validity__icontains=query) |
            Q(scheme__icontains=query)
        )
    else:
        discharged_member = Discharged.objects.all()
    return render(request, 'Discharged_list.html', {'discharged_member': discharged_member, 'query': query})


def readmit(request, pk):
    discharged = get_object_or_404(Discharged, pk=pk)
    MemberDetail.objects.create(
        first_name=discharged.first_name,
        last_name=discharged.last_name,
        payer=discharged.payer,
        membership_number=discharged.membership_number,
        relationship=discharged.relationship,
        validity=discharged.validity,
        scheme=discharged.scheme,
    )
    discharged.delete()
    return redirect('index')
 
 #**************************************************************************************************************************************************
def pending_admissions(request):
    query = request.GET.get('q')
    payer_filter = request.GET.get('payer')
    scheme_filter = request.GET.get('scheme')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    order = request.GET.get('order', 'added_at')

    pending_members = Member_Detail.objects.filter(admission_status= 'pending')

    if query:
        pending_members = pending_members.filter(
            Q(name__icontains=query) |
            Q(membership_number__icontains=query)
        )
    if payer_filter:
        pending_members = pending_members.filter(payer__icontains=payer_filter)
    if scheme_filter:
        pending_members = pending_members.filter(scheme__icontains=scheme_filter)
    if date_from:
        pending_members = pending_members.filter(added_at__gte=parse_date(date_from))
    if date_to:
        pending_members = pending_members.filter(added_at__lte=parse_date(date_to))

    pending_members = pending_members.order_by(order)
    
    return render(request, 'pending_admissions/pending_admissions.html', 
                  {'pending_members': pending_members, 
                    'query': query, 'payer_filter': payer_filter, 
                    'scheme_filter': scheme_filter, 
                    'date_from': date_from, 'date_to': date_to, 
                    'order': order})

def admit_pending_member(request, pk):
    admission = get_object_or_404(Member_Detail, pk=pk)

    discharge = Discharge.objects.create(
        first_name=admission.name,
        payer=admission.payer,
        membership_number=admission.membership_number,
        relationship=admission.relationship,
        validity=admission.validity,
        scheme=admission.scheme,
    )
    admission.delete()

    return redirect("discharge_member_detail", pk=discharge.pk)

def admitting_member_detail(request, pk):
    member = get_object_or_404(Member_Detail, pk=pk)
    insurance_details = InsuranceDetail.objects.filter(member=member)
    try:
        scheme = Scheme.objects.get(name=member.scheme)
        providers = scheme.providers.all()
    except Scheme.DoesNotExist:
        # Scheme is not registered
        scheme = None
        providers = []

    return render(request, 'pending_admissions/admitting_member_detail.html', 
                  {'member': member, 
                   'insurance_details': insurance_details,
                   'scheme': scheme,
                   'providers': providers
                   })

def admit_member(request, pk):
    member = get_object_or_404(Member_Detail, pk=pk)
    providers = Provider.objects.all()
    insurance_details = member.insurance_details.all()

    if request.method == 'POST':
        service_provider_id = request.POST.get('service_provider')
        admission_date = request.POST.get('admission_date')
        admission_diagnosis = request.POST.get('admission_diagnosis')
        cover_used_id = request.POST.get('cover_used')
        initial_cover_value = request.POST.get('initial_cover_value')
        initial_cover_balance = request.POST.get('initial_cover_balance')
        requested_amount = request.POST.get('requested_amount')
        lou_issued = request.POST.get('lou_issued')

        # Get the selected provider and cover
        provider = get_object_or_404(Provider, pk=service_provider_id)
        cover_used = get_object_or_404(insurance_details, pk=cover_used_id)

        # Save the admission details
        admission_detail = Admission_details(
            member=member,
            Provider=provider,
            admission_date=admission_date,
            admission_diagnosis=admission_diagnosis,
            cover_used=cover_used.cover_type,
            initial_cover_value=initial_cover_value,
            initial_cover_balance=initial_cover_balance,
            requested_amount=requested_amount,
            lou_issued=lou_issued,
            admited_by=request.user.username  # Assuming you have the user authenticated
        )
        member.admission_status = 'admitted'
        member.save()
        admission_detail.save()

        # messages.success(request, 'Admission details saved successfully.')
        return redirect('pending_admissions')  # Redirect to a success page or admission summary

    return render(request, 'pending_admissions/pending_admissions.html', {
        'member': member,
        'providers': providers,
        'insurance_details': insurance_details,
    })

