from django.urls import path
from .views import (
    admit_member, 
    index, member_detail, 
    discharge_list, 
    discharge_member, 
    discharge_member_detail, 
    undo_admit_member, 
    undo_discharge_member, 
    discharged_list, 
    discharged_member_detail, 
    pending_admissions
    )
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('member/<int:pk>/', member_detail, name='member_detail'),
    path('member/<int:pk>/admit/', admit_member, name='admit_member'),
    path('discharge/', discharge_list, name='discharge_list'),
    path('discharge/<int:pk>/', discharge_member_detail, name='discharge_member_detail'),
    path('discharge/<int:pk>/discharge/', discharge_member, name='discharge_member'),
    path('undo_admit_member/<int:pk>/', undo_admit_member, name='undo_admit_member'),
    path('undo_discharge_member/<int:pk>/', undo_discharge_member, name='undo_discharge_member'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('pending_admissions/', views.pending_admissions, name='pending_admissions'),
    path('admitting_member_detail/<int:pk>/', views.admitting_member_detail, name='admitting_member_detail'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('discharged/', discharged_list, name='discharged_list'),
    path('discharged/<int:pk>/', discharged_member_detail, name='dis'),
    path('readmit/<int:pk>/', views.readmit, name='readmit'),
    path('admit_member/<int:pk>/', views.admit_member, name='admit_member'),
    path('', index, name='index'),
]