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
from .forms import UpdateForm
import tempfile
import io
from django.http import FileResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import (
    Member_Detail, 
    InsuranceDetail,
    Scheme,
    Provider,
    Admission_details,
    Discharge_details,
    Daily_update
    )

 #**************************************************************************************************************************************************
def pending_admissions(request): #list of recently imported, awaiting admission.
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
    except Scheme.DoesNotExist: # if the scheme is not registered then shown an empty list of the providers.
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

        # Get the selected provider and cover used
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
            admited_by=request.user.username  #registering the authenticated user
        )
        member.admission_status = 'admitted'
        member.save()
        admission_detail.save()

        return redirect('current_admissions')  # Redirect to the list of current admissions page or admission summary - an LOU generation page to be added before proceeding to the list of currently admitted members.

    return render(request, 'currently_admitted/currently_admitted.html', {
        'member': member,
        'providers': providers,
        'insurance_details': insurance_details,
    })

# @login_required
# def generate_admission_pdf(request, pk):
    # Retrieve member and related details
    member = get_object_or_404(Member_Detail, pk=pk)
    admission_details = Admission_details.objects.filter(member=member).first()
    discharge_details = Discharge_details.objects.filter(member=member).last()

    # Retrieve updates
    updates = Daily_update.objects.filter(admission=admission_details).order_by('-date')

    # Context for rendering the PDF
    context = {
        'member': member,
        'admission_details': admission_details,
        'discharge_details': discharge_details,
        'updates': updates,
        'current_date': timezone.now().date(),
    }

    # Render the HTML template to a string
    html_string = render_to_string('currently_admitted/discharge_summary.html', context)

    # Generate the PDF in memory using BytesIO
    pdf_io = io.BytesIO()
    HTML(string=html_string).write_pdf(target=pdf_io)

    # Rewind the BytesIO object to the beginning
    pdf_io.seek(0)

    # Create a FileResponse for downloading the PDF
    response = FileResponse(pdf_io, as_attachment=True, filename=f'Discharge_Summary_{member.name}.pdf')

    # Return the FileResponse
    return response

    # After returning the PDF response, redirect to the discharged_members page
    return HttpResponseRedirect(reverse('discharged_members'))


def current_admissions(request): #active admissions list. 
    query = request.GET.get('q')
    payer_filter = request.GET.get('payer')
    scheme_filter = request.GET.get('scheme')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    order = request.GET.get('order', 'added_at')

    admitted_members = Member_Detail.objects.filter(admission_status= 'admitted') #filtering the admitted members


    if query: #filtering by name or membership number
        admitted_members = admitted_members.filter(
            Q(name__icontains=query) |
            Q(membership_number__icontains=query)
        )
    if payer_filter: #filtering by payer
        admitted_members = admitted_members.filter(payer__icontains=payer_filter)

    if scheme_filter: #filtering by scheme
        admitted_members = admitted_members.filter(scheme__icontains=scheme_filter)

    if date_from:  #filtering by date
        admitted_members = admitted_members.filter(admission_details__admission_date__gte=parse_date(date_from))

    if date_to: #filtering by date
        admitted_members = admitted_members.filter(admission_details__admission_date__lte=parse_date(date_to))

    admitted_members = admitted_members.order_by(order) #sorting by date
    
    return render(request, 'currently_admitted/currently_admitted.html', 
                  {'admitted_members': admitted_members, 
                    'query': query, 'payer_filter': payer_filter, 
                    'scheme_filter': scheme_filter, 
                    'date_from': date_from, 'date_to': date_to, 
                    'order': order})

def discharging_member_detail(request, pk): #page displaying details of the member to be discharged.
    member = get_object_or_404(Member_Detail, pk=pk)
    admission_details = Admission_details.objects.filter(member=member).first()

     #calculating the number of days since admission
    days_since_admission = None
    if admission_details and admission_details.admission_date:
        current_date = now().date() 
        admission_date = admission_details.admission_date
        days_since_admission = (current_date - admission_date).days

    context = {
        'member': member,
        'admission_details': admission_details,
        'days_since_admission': days_since_admission,
        } #context variables

    return render(request, 'currently_admitted/discharge_member.html', context)

@login_required
def discharge_member(request, pk):  #discharge a member button
    member = get_object_or_404(Member_Detail, pk=pk)
    admission_details = Admission_details.objects.filter(member=member).first()
    update_form = UpdateForm(request.POST or None)

    # Handle form submissions for daily updates
    if request.method == 'POST':
        if 'add_update' in request.POST: #saving to Daily_update object.          
            if update_form.is_valid(): # Create and save the update
                update = update_form.save(commit=False)
                update.admission = admission_details
                update.save()

                #redirect to the same page to show the new update
                return redirect('discharging_member_detail', pk=pk)
        
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

            return redirect('generate_discharge_pdf', pk=pk)  # Redirect to a discharged_members page - will add LOU generation 

   
    # Retrieve existing daily updates for this admission
    updates = Daily_update.objects.filter(admission=admission_details).order_by('-date')


    context = {
        'member': member,
        'admission_details': admission_details,
        'updates': updates,
        'update_form': update_form,
        'current_date': timezone.now().date(),
    }

    return render(request, 'discharged/discharged_members.html', context)

@login_required
def generate_discharge_pdf(request, pk):
    # Retrieve member and related details
    member = get_object_or_404(Member_Detail, pk=pk)
    admission_details = Admission_details.objects.filter(member=member).first()
    discharge_details = Discharge_details.objects.filter(member=member).last()

    # Retrieve updates
    updates = Daily_update.objects.filter(admission=admission_details).order_by('-date')

    # Context for rendering the PDF
    context = {
        'member': member,
        'admission_details': admission_details,
        'discharge_details': discharge_details,
        'updates': updates,
        'current_date': timezone.now().date(),
    }

    # Render the HTML template to a string
    html_string = render_to_string('currently_admitted/discharge_summary.html', context)

    # Generate the PDF in memory using BytesIO
    pdf_io = io.BytesIO()
    HTML(string=html_string).write_pdf(target=pdf_io)

    # Rewind the BytesIO object to the beginning
    pdf_io.seek(0)

    # Create a FileResponse for downloading the PDF
    response = FileResponse(pdf_io, as_attachment=True, filename=f'Discharge_Summary_{member.name}.pdf')

    # Return the FileResponse
    return response


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
    discharge_entry = get_object_or_404(
        Discharge_details.objects.select_related('member'), 
        pk=discharge_id
    )

    # Fetch the member's previous admissions using Discharge_details model
    previous_admissions = Discharge_details.objects.filter(member=discharge_entry.member)

    context = {
        'member': discharge_entry.member,
        'discharge_entry': discharge_entry,
        'previous_admissions': previous_admissions,
    }
    
    return render(request, 'discharged/admission_history.html', context)
