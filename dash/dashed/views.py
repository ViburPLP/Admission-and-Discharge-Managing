from django.shortcuts import render, get_object_or_404, redirect
from .models import Discharge, MemberDetail, Discharged
from django.contrib.auth.decorators import login_required
from django.db.models import Q



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
    if query:
        members = MemberDetail.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(payer__icontains=query) |
            Q(membership_number__icontains=query) |
            Q(relationship__icontains=query) |
            Q(validity__icontains=query) |
            Q(scheme__icontains=query)
        )
    else:
        members = MemberDetail.objects.all()
    return render(request, 'index.html', {'members': members, 'query': query})

@login_required
def discharge_list(request):
    query = request.GET.get('q')
    if query:
        discharges = Discharge.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(payer__icontains=query) |
            Q(membership_number__icontains=query) |
            Q(relationship__icontains=query) |
            Q(validity__icontains=query) |
            Q(scheme__icontains=query)
        )
    else:
        discharges = Discharge.objects.all()
    return render(request, 'discharge.html', {'discharges': discharges, 'query': query})

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
