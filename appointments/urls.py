from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('list/', views.appointment_list, name='appointment_list'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('get_available_time_slots/', views.get_available_time_slots, name='get_available_time_slots'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('edit_appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/', views.view_appointments, name='view_appointments')
]
