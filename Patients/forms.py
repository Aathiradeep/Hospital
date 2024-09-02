# Patients/forms.py
from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'phone_number', 'doctor', 'patient_address', 'medical_history']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'patient_address', 'medical_history', 'profile_picture']

class EditPatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'patient_address', 'medical_history', 'profile_picture']