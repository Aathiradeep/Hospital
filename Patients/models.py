# Patients/models.py
from django.db import models
from django.contrib.auth.models import User
from Doctors.models import Doctor

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default="Unknown")     
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    patient_address = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    current_medication = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username if self.user else "Unlinked Patient"
