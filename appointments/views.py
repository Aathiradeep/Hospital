from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Doctors.models import Doctor
from datetime import datetime, date
from django.http import JsonResponse
from .utils import generate_time_slots
from Patients.models import Patient
from Billing.models import Bill
from django.utils.timezone import now

@login_required
def patient_dashboard(request):
    available_doctors = Doctor.objects.all()
    today = date.today()
    patient = request.user.patient

    # Fetch the patient's appointments
    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'time')

    # Fetch bills for the patient
    bills = Bill.objects.filter(patient=request.user.patient).order_by('-date_generated')

    # Render the template for the initial page load
    return render(request, 'patient_dashboard.html', {
        'available_doctors': available_doctors,
        'appointments': appointments,
        'today': today,
        'bills': bills,
    })

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient

            # Ensure patient has a phone attribute
            if hasattr(appointment.patient, 'phone'):
                patient_phone = appointment.patient.phone
            else:
                # Handle case where phone is not available
                phone_number = "Phone not available"

            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('patient_dashboard')  # Ensure this URL name is correct
        else:
            messages.error(request, "Failed to book appointment. Please correct the errors below.")
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})

@login_required
def get_available_time_slots(request):
    doctor_id = request.GET.get('doctor_id')
    selected_date = request.GET.get('date')

    doctor = get_object_or_404(Doctor, id=doctor_id)
    booked_slots = Appointment.objects.filter(doctor=doctor, date=selected_date).values_list('time', flat=True)

    available_time_slots = generate_time_slots(doctor.working_hours_start, doctor.working_hours_end)
    available_time_slots = [slot for slot in available_time_slots if slot not in booked_slots]

    return JsonResponse({'available_time_slots': available_time_slots})

@login_required
def appointment_list(request):
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all().order_by('date', 'time')

    doctor_id = request.GET.get('doctor')
    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)

    selected_date = request.GET.get('date')
    if selected_date:
        try:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            appointments = appointments.filter(date=date_obj)
        except ValueError:
            pass

    context = {
        'appointments': appointments,
        'doctors': doctors,
        'selected_doctor': doctor_id,
        'selected_date': selected_date,
    }

    return render(request, 'appointment_list.html', context)

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user == appointment.patient.user or request.user == appointment.doctor.user or request.user.is_superuser:
        return render(request, 'appointment_detail.html', {'appointment': appointment})
    else:
        messages.error(request, "You are not authorized to view this appointment.")
        return redirect('appointment_list')

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment canceled successfully.')

        if request.user.groups.filter(name='Doctor').exists():
            return redirect('doctor_dashboard')
        elif request.user.groups.filter(name='Patient').exists():
            return redirect('patient_dashboard')
        else:
            return redirect('appointment_list')

    return render(request, 'cancel_appointment.html', {'appointment': appointment})

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'edit_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def patient_bills(request):
    bills = Bill.objects.filter(patient=request.user.patient)
    return render(request, 'patient_bills.html', {'bills': bills})

@login_required
def doctor_bills(request):
    bills = Bill.objects.filter(doctor=request.user.doctor)
    return render(request, 'doctor_bills.html', {'bills': bills})

@login_required
def mark_notification_seen(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        appointment.notification_seen = True
        appointment.save()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'failure'})

@login_required
def view_appointments(request):
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'time')
    return render(request, 'view_appointments.html', {'appointments': appointments})


