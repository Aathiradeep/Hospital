# Patients/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),  # Patient list
    path('<int:patient_id>/', views.patient_detail, name='patient_detail'),  # Patient detail
    path('<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),  # Edit patient
    path('<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),  # Delete patient
    path('profile/', views.patient_profile, name='patient_profile'),
    path('appointments/', views.patient_appointments, name='patient_appointments'),
    path('profile/edit/<int:patient_id>/', views.edit_patient_profile, name='edit_patient_profile'),
]
