from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Department
from .forms import DoctorForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from Billing.models import Bill  # Adjust the import path as needed
from django.utils.timezone import now
from datetime import timedelta, datetime, date


# Doctor Dashboard
@login_required
def doctor_dashboard(request):
    doctor = request.user.doctor
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date')
    billing = Bill.objects.filter(doctor=doctor).order_by('-date_generated').first()

    # Example of additional data processing or filtering if needed
    today = now().date()
    upcoming_appointments = appointments.filter(date__gte=today)

    context = {
        'appointments': appointments,
        'upcoming_appointments': upcoming_appointments,
        'billing': billing,
    }
    return render(request, 'doctor_dashboard.html', context)


# Check Doctor Availability
def check_doctor_availability(doctor):
    now_time = now()
    next_30_minutes = now_time + timedelta(minutes=30)

    if not Appointment.objects.filter(
            doctor=doctor,
            date=now_time.date(),
            time__range=(now_time.time(), next_30_minutes.time())
    ).exists():
        return True
    return False


# List All Doctors
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})


# View Details of a Specific Doctor
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor_detail.html', {'doctor': doctor})


# Add a New Doctor
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor successfully added!')
            return redirect('doctor_list')  # Redirect to the list of doctors after saving
    else:
        form = DoctorForm()

    return render(request, 'add_doctor.html', {'form': form})


# Doctor Profile (Private View for Logged-In Doctor)
@login_required
def doctor_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    return render(request, 'doctor_profile.html', {'doctor': doctor})


# Public Doctor Profile (Viewable by Anyone)
def public_doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor_profile.html', {'doctor': doctor})

def doctor_appointments(request):
    doctor = request.user.doctor
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = Appointment.objects.filter(doctor=doctor, status=status_filter).order_by('-date')
    else:
        appointments = Appointment.objects.filter(doctor=doctor).order_by('-date')
    
    return render(request, 'doctor_appointments.html', {'appointments': appointments})

@login_required
def update_appointment_status(request, appointment_id):
    if request.method == 'POST':
        appointment = Appointment.objects.get(id=appointment_id)
        new_status = request.POST.get('status')
        appointment.status = new_status
        appointment.save()
        
        messages.success(request, 'Appointment status updated successfully.')
    
    return redirect('doctor_appointments')