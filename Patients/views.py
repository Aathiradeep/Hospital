# Patients/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, EditPatientProfileForm
from django.contrib import messages
from appointments.models import Appointment
from Doctors.models import Doctor
from datetime import date, timedelta, datetime
from appointments.utils import get_available_time_slots
from django.utils.timezone import now

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def patient_detail(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    return render(request, 'patient_detail.html', {'patient': patient})

def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient details updated successfully!')
            return redirect('patient_list')  # Ensure this URL pattern matches
    else:
        form = PatientForm(instance=patient)
    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
        return redirect('patient_list')

    return render(request, 'delete_patient.html', {'patient': patient}) 

@login_required
def patient_profile(request):
    patient = get_object_or_404(Patient, user=request.user)
    return render(request, 'patient_profile.html', {'patient': patient})

@login_required
def patient_appointments(request):
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient).order_by('-date')
    return render(request, 'patient_appointments.html', {'appointments': appointments})

@login_required
def edit_patient_profile(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = EditPatientProfileForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('patient_profile')  # Adjust this redirect to match the actual profile URL name
    else:
        form = EditPatientProfileForm(instance=patient)
    
    return render(request, 'edit_patient_profile.html', {'form': form, 'patient': patient})