from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.utils.dateparse import parse_date
from datetime import datetime
from django.utils.timezone import now
from django.utils import timezone
from .forms import UpdateForm
from .models import (
    Discharge, 
    MemberDetail, 
    Discharged, 
    Member_Detail, 
    InsuranceDetail,
    Scheme,
    Provider,
    Admission_details,
    Discharge_details,
    Daily_update
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

def discharge_member1(request, pk):
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
def pending_admissions(request): #members waiting to be admitted- recently imported members
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


def admitting_member_detail(request, pk): #page displaying details of the member to be admited.
    member = get_object_or_404(Member_Detail, pk=pk)
    insurance_details = InsuranceDetail.objects.filter(member=member)
    try:
        scheme = Scheme.objects.get(name=member.scheme)
        providers = scheme.providers.all()
    except Scheme.DoesNotExist: # if the scheme is not registered then shown an empty list of the providers----
        scheme = None
        providers = []

    return render(request, 'pending_admissions/admitting_member_detail.html', 
                  {'member': member, 
                   'insurance_details': insurance_details,
                   'scheme': scheme,
                   'providers': providers
                   })

def admit_member(request, pk): # Updated The button to admit a member
    member = get_object_or_404(Member_Detail, pk=pk)
    providers = Provider.objects.all()
    insurance_details = member.insurance_details.all()

    if request.method == 'POST':
        service_provider_id = request.POST.get('service_provider')
        admission_date = request.POST.get('admission_date')
        admission_diagnosis = request.POST.get('admission_diagnosis_description')
        cover_used_id = request.POST.get('cover_used')
        initial_cover_value = request.POST.get('initial_cover_value')
        initial_cover_balance = request.POST.get('initial_cover_balance')
        requested_amount = request.POST.get('requested_amount')
        lou_issued = request.POST.get('lou_issued')

        # Get the selected provider and cover
        provider = get_object_or_404(Provider, pk=service_provider_id)
        cover_used = get_object_or_404(insurance_details, pk=cover_used_id)

        # Save the admission details to a different table. 
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
        return redirect('current_admissions')  # Redirect to a success page or admission summary

    return render(request, 'currently_admitted/currently_admitted.html', {
        'member': member,
        'providers': providers,
        'insurance_details': insurance_details,
    })

def current_admissions(request): # list of members already admitted or awaiting discharge. 
    query = request.GET.get('q')
    payer_filter = request.GET.get('payer')
    scheme_filter = request.GET.get('scheme')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    order = request.GET.get('order', 'added_at')

    admitted_members = Member_Detail.objects.filter(admission_status= 'admitted')


    if query:
        admitted_members = admitted_members.filter(
            Q(name__icontains=query) |
            Q(membership_number__icontains=query)
        )
    if payer_filter:
        admitted_members = admitted_members.filter(payer__icontains=payer_filter)
    if scheme_filter:
        admitted_members = admitted_members.filter(scheme__icontains=scheme_filter)
    if date_from:
        admitted_members = admitted_members.filter(admission_details__admission_date__gte=parse_date(date_from))
    if date_to:
        admitted_members = admitted_members.filter(admission_details__admission_date__lte=parse_date(date_to))

    admitted_members = admitted_members.order_by(order)
    
    return render(request, 'currently_admitted/currently_admitted.html', 
                  {'admitted_members': admitted_members, 
                    'query': query, 'payer_filter': payer_filter, 
                    'scheme_filter': scheme_filter, 
                    'date_from': date_from, 'date_to': date_to, 
                    'order': order})

def discharging_member_detail(request, pk): #page displaying details of the member to be discharged.
    member = get_object_or_404(Member_Detail, pk=pk)
    admission_details = Admission_details.objects.filter(member=member).first()

     # Calculating the number of days since admission
    days_since_admission = None
    if admission_details and admission_details.admission_date:
        current_date = now().date() 
        admission_date = admission_details.admission_date
        days_since_admission = (current_date - admission_date).days

    context = {
        'member': member,
        'admission_details': admission_details,
        'days_since_admission': days_since_admission,
        }

    return render(request, 'currently_admitted/discharge_member.html', context)

from .forms import UpdateForm

@login_required
def discharge_member(request, pk):  #discharge a member button
    member = get_object_or_404(Member_Detail, pk=pk)
    admission_details = Admission_details.objects.filter(member=member).first()
    update_form = UpdateForm(request.POST or None)

    # Handle form submissions for daily updates
    if request.method == 'POST':
        if 'add_update' in request.POST:
            # Handle daily update form submission
            # update_form = UpdateForm(request.POST)
            
            if update_form.is_valid():
                # Create and save the update
                update = update_form.save(commit=False)
                update.admission = admission_details
                update.save()

                # Redirect to the same page to show the new update
                return redirect('discharge_member', pk=pk)
        
        elif 'discharge_member_form' in request.POST:
            # Saving to Discharge_details object
            discharge_details = Discharge_details(
                member=member,
                provider=admission_details.Provider,
                admission_date=admission_details.admission_date,
                admission_diagnosis=admission_details.admission_diagnosis,
                cover_used=admission_details.cover_used,
                initial_cover_value=admission_details.initial_cover_value,
                initial_cover_balance=admission_details.initial_cover_balance,
                requested_amount=admission_details.requested_amount,
                lou_issued=admission_details.lou_issued,
                admitted_by=admission_details.admited_by,
                relationship=member.relationship,
                name=member.name,
                membership_number=member.membership_number,
                payer=member.payer,
                scheme=member.scheme,
                status=member.status,
                validity=member.validity,
                discharge_date=request.POST.get('discharge_date', timezone.now()),
                discharge_summary=request.POST.get('discharge_summary', ''),
                final_approved_amount=request.POST.get('final_approved_amount', ''),
                discharge_notes=request.POST.get('discharge_notes', ''),
                discharged_by=request.POST.get('discharged_by', request.user.username)
            )
            
            discharge_details.save()

            # Update member status to discharged
            member.admission_status = 'discharged'
            member.save()

            return redirect('current_admissions')  # Redirect to a success page or the member list

    # else:
    #     update_form = UpdateForm()

    # Retrieve existing daily updates for this admission
    updates = Daily_update.objects.filter(admission=admission_details).order_by('-date')

    # Get available providers for display in form
    providers = Provider.objects.all()

    context = {
        'member': member,
        'admission_details': admission_details,
        'providers': providers,
        'updates': updates,
        'update_form': update_form,
        'current_date': timezone.now().date(),
    }

    return render(request, 'discharged/discharge_member.html', context)

# def discharged_members(request): # list of members already discharged. 
#     query = request.GET.get('q')
#     payer_filter = request.GET.get('payer')
#     scheme_filter = request.GET.get('scheme')
#     date_from = request.GET.get('date_from')
#     date_to = request.GET.get('date_to')
#     order = request.GET.get('order', 'added_at')

#     discharged_members = Member_Detail.objects.filter(admission_status= 'discharged')


#     if query:
#         discharged_members = discharged_members.filter(
#             Q(name__icontains=query) |
#             Q(membership_number__icontains=query)
#         )
#     if payer_filter:
#         discharged_members = discharged_members.filter(payer__icontains=payer_filter)
#     if scheme_filter:
#         discharged_members = discharged_members.filter(scheme__icontains=scheme_filter)
#     if date_from:
#         discharged_members = discharged_members.filter(discharge_details__discharge_date__gte=parse_date(date_from))
#     if date_to:
#         discharged_members = discharged_members.filter(discharge_details__discharge_date__lte=parse_date(date_to))

#     discharged_members = discharged_members.order_by(order)
    
#     return render(request, 'discharged/discharged_members.html', 
#                   {'discharged_members': discharged_members, 
#                     'query': query, 'payer_filter': payer_filter, 
#                     'scheme_filter': scheme_filter, 
#                     'date_from': date_from, 'date_to': date_to, 
#                     'order': order})

from django.shortcuts import render
from django.db.models import Q
from django.utils.dateparse import parse_date
from .models import Discharge_details

def discharged_members(request): 
    query = request.GET.get('q')
    payer_filter = request.GET.get('payer')
    scheme_filter = request.GET.get('scheme')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    order = request.GET.get('order', '-discharge_date')  # Default order field

    discharged_entries = Discharge_details.objects.all()  # Get all discharge entries

    # Filtering based on search query
    if query:
        discharged_entries = discharged_entries.filter(
            Q(name__icontains=query) |
            Q(membership_number__icontains=query)
        )
    
    # Filtering based on payer
    if payer_filter:
        discharged_entries = discharged_entries.filter(payer__icontains=payer_filter)
    
    # Filtering based on scheme
    if scheme_filter:
        discharged_entries = discharged_entries.filter(scheme__icontains=scheme_filter)
    
    # Filtering based on discharge date
    if date_from:
        try:
            date_from = parse_date(date_from)
            discharged_entries = discharged_entries.filter(discharge_date__gte=date_from)
        except ValueError:
            # Handle invalid date format
            pass
    
    if date_to:
        try:
            date_to = parse_date(date_to)
            discharged_entries = discharged_entries.filter(discharge_date__lte=date_to)
        except ValueError:
            # Handle invalid date format
            pass

    # Ensure ordering field is valid
    valid_order_fields = ['discharge_date', 'membership_number', 'name', 'payer', 'scheme']
    if order not in valid_order_fields:
        order = '-discharge_date'

    discharged_entries = discharged_entries.order_by(order)

    context = {
        'discharged_entries': discharged_entries,
        'query': query,
        'payer_filter': payer_filter,
        'scheme_filter': scheme_filter,
        'date_from': date_from,
        'date_to': date_to,
        'order': order,
    }

    return render(request, 'discharged/discharged_members.html', context)


def admission_history(request, discharge_id):
    # Get the discharge details based on the ID
    discharge_entry = get_object_or_404(Discharge_details, pk=discharge_id)

    # Fetch the member's previous admissions
    previous_admissions = Admission_details.objects.filter(member=discharge_entry.member)

    context = {
        'member': discharge_entry.member,
        'discharge_entry': discharge_entry,
        'previous_admissions': previous_admissions,
    }
    
    return render(request, 'discharged/admission_history.html', context)