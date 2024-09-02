from django.urls import path
from . import views
from .views import patient_bills

urlpatterns = [
    path('generate_bill/', views.generate_bill, name='generate_bill'),
    path('bills/', patient_bills, name='patient_bills'),   
    path('doctor_bills/', views.doctor_bills, name='doctor_bills'),
    path('billing_list/', views.billing_list, name='billing_list'),
    path('download_pdf/<int:billing_id>/', views.download_pdf, name='download_pdf'),
    path('get_patient_details/<int:patient_id>/', views.get_patient_details, name='get_patient_details'),  # Correct endpoint
    path('billing/<int:billing_id>/', views.billing_detail, name='billing_detail'),  # Correcting the pattern to include the billing ID
]
