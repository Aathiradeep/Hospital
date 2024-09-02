from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'email', 'phone_number', 'experience', 'qualifications', 'image', 'department','working_hours_start','working_hours_end']
