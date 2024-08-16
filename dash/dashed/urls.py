from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    #start here
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'), #login page
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), #logout page


    #pages in order or flow of activity
    path('pending_admissions/', views.pending_admissions, name='pending_admissions'), #list of recently imported, awaiting admission.
    path('admitting_member_detail/<int:pk>/', views.admitting_member_detail, name='admitting_member_detail'), #page displaying details of the member to be admited.
    path('admit_member/<int:pk>/', views.admit_member, name='admit_member'), #admit member 'button'.
    # path('generate_admission_pdf/<int:pk>/', views.generate_admission_pdf, name='generate_admission_pdf'),	
    
    path('currently_admitted/', views.current_admissions, name='current_admissions'), #active admissions list.
    path('discharging_member_detail/<int:pk>/', views.discharging_member_detail, name='discharging_member_detail'), #page displaying details of the active admission- for discharge or updates.
    path('discharge_member<int:pk>/', views.discharge_member, name='discharge_member'), #discharge member 'button'.
    path('generate_discharge_pdf/<int:pk>/', views.generate_discharge_pdf, name='generate_discharge_pdf'),

    path('discharged_members/', views.discharged_members, name='discharged_members'), #discharged members list.
    path('admission_history/<int:discharge_id>/', views.admission_history, name='admission_history'), #page with details of previous admissions.
]
