# views.py
from django.shortcuts import render
from Billing.models import Bill
from Patients.models import Patient
from Doctors.models import Doctor
from appointments.models import Appointment
from django.db.models import Sum

def report_detail(request):
    # Example code to use the Report model
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()  # Replace with actual model if needed
    total_revenue = Bill.objects.aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0

    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_revenue': total_revenue,
    }

    return render(request, 'report_detail.html', context)
