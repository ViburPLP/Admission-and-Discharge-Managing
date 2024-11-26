from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    #start here
    path('accounts/login/', LoginView.as_view(template_name='template/user/log-in.html', next_page='home'), name='login'), #login page
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), #logout page


    #home/landing
    path('', views.home, name='home'),

    #admissions
        #pending-admitting
    path('pending_admissions/', views.pending_admissions, name='pending_admissions'), #list of recently imported, awaiting admission.
    path('admitting_member_detail/<int:pk>/', views.admitting_member_detail, name='admitting_member_detail'), #page displaying details of the member to be admited.
    path('admit_member/<int:pk>/', views.admit_member, name='admit_member'), #admit member 'button'.

        #active-admissions
    path('currently_admitted/', views.current_admissions, name='current_admissions'), #active admissions list.
    path('discharging_member_detail/<int:pk>/', views.discharging_member_detail, name='discharging_member_detail'), #page displaying details of the active admission- for discharge or updates.
    path('discharge_member<int:pk>/', views.discharge_member, name='discharge_member'), #discharge member 'button'.

        #discharged
    path('discharged_members/', views.discharged_members, name='discharged_members'), #discharged members list.
    path('admission_history/<int:discharge_id>/', views.admission_history, name='admission_history'), #page with details of previous admissions.

    #reports
    path('trend-analysis/', views.trend_analysis, name='trend_analysis'),
    path('reports/', views.reports, name='reports'),
    path('payer_reports/<str:payer_name>/', views.payer_reports, name='payer_reports'),
    path('export_report/<str:payer_name>/', views.export_payer_report, name='export_payer_report'),

    # account
    path('account/', views.user_account, name='user_account'),
    path('account/update/', views.update_user_details, name='update_user_details'),
    path('account/change-password/', views.change_password, name='change_password'),

    #schemes and providers management
    path('schemes/', views.schemes, name='schemes'),
    path('scheme_detail/<int:scheme_id>/', views.scheme_detail, name='scheme_detail'),

    path('manage/', views.manage_schemes_providers, name='manage_schemes_providers'),
    path('edit-scheme/<int:scheme_id>/', views.edit_scheme, name='edit_scheme'),
    path('delete-scheme/<int:scheme_id>/', views.delete_scheme, name='delete_scheme'),
    path('view-providers/<int:scheme_id>/', views.view_providers, name='view_providers'),
    path('edit-provider/<int:provider_id>/', views.edit_provider, name='edit_provider'),
    path('delete-provider/<int:provider_id>/', views.delete_provider, name='delete_provider'),
    path('view-schemes/<int:provider_id>/', views.view_schemes, name='view_schemes'),

    path('providers/', views.providers, name='providers'),
    path('provider_detail/<int:provider_id>/', views.provider_detail, name='provider_detail'),



    path('trend-analysis/', views.trend_analysis, name='trend_analysis'),
            
    ]


