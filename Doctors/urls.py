from django.urls import path
from . import views
from Billing.views import billing_detail  # Import the view if it's in a different app

urlpatterns = [
    # Doctor's dashboard and profile
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/profile/', views.doctor_profile, name='doctor_profile'),
    
    # Public doctor-related paths
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('add/', views.add_doctor, name='add_doctor'),
    path('doctor/<int:doctor_id>/', views.public_doctor_profile, name='public_doctor_profile'),

    # Appointment-related paths
    path('doctor_appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('update_appointment_status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),    
    # Billing-related paths
    #path('billing/<int:patient_id>/', billing_detail, name='billing_detail'),  # Corrected path
]
