from .models import Appointment
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models

from django.utils import timezone
from Patients.models import Patient
from Doctors.models import Doctor
from Billing.models import Bill
from Reports.models import Report




def generate_time_slots(start_time, end_time, interval=15):
    slots = []
    current_time = datetime.combine(datetime.today(), start_time)
    end_time = datetime.combine(datetime.today(), end_time)

    while current_time < end_time:
        slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=interval)

    return slots

def get_available_time_slots(doctor, selected_date):
    # Generate all possible time slots for the doctor's working hours
    all_time_slots = generate_time_slots(doctor.working_hours_start, doctor.working_hours_end)

    # Get the already booked time slots for this doctor on the selected date
    booked_slots = Appointment.objects.filter(doctor=doctor, date=selected_date).values_list('time', flat=True)

    # Filter out the booked slots from the generated slots
    available_time_slots = [slot for slot in all_time_slots if slot not in booked_slots]

    return available_time_slots

def get_dashboard_url(user: User) -> str:
    """Determines the correct dashboard URL based on user type."""
    if user.groups.filter(name='Doctor').exists():
        return 'doctor_dashboard'
    elif user.groups.filter(name='Patient').exists():
        return 'patient_dashboard'
    elif user.is_superuser:
        return 'admin_dashboard'
    return None


def generate_hospital_report(start_date, end_date):
    total_patients = Patient.objects.filter(registered_on__range=[start_date, end_date]).count()
    total_appointments = Appointment.objects.filter(date__range=[start_date, end_date]).count()
    total_doctors = Doctor.objects.count()
    total_revenue = Bill.objects.filter(date__range=[start_date, end_date]).aggregate(total=models.Sum('amount'))['total'] or 0

    report = Report.objects.create(
        start_date=start_date,
        end_date=end_date,
        total_patients=total_patients,
        total_appointments=total_appointments,
        total_doctors=total_doctors,
        total_revenue=total_revenue
    )
    return report

