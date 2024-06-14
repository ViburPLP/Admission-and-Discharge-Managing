from django.urls import path
from . import views

urlpatterns = [
    path('pending/', views.pending_admissions, name='pending_admissions'),
    path('admit/<str:membership_number>/', views.admit_patient, name='admit_patient'),
]
