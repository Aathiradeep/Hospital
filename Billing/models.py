from django.db import models
from Patients.models import Patient
from Doctors.models import Doctor
from decimal import Decimal


class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_phone = models.CharField(max_length=15, null=True, blank=True)  # Allowing null values
    patient_address = models.TextField(null=True, blank=True)  # Allowing null values
    room_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    medicine_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    days_stayed = models.IntegerField(default=0)
    date_generated = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Allow null and blank
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def calculate_total(self):

        # Retrieve consultation fee from the associated doctor
        consultation_fee = Decimal(self.doctor.consultation_fee)
        # Convert all fields to Decimal
        room_charge = Decimal(self.room_charge)
        medicine_cost = Decimal(self.medicine_cost or 0)
        other_charges = Decimal(self.other_charges or 0)
        days_stayed = Decimal(self.days_stayed)
        consultation_fee = Decimal(self.consultation_fee)

        # Perform calculations
        total = consultation_fee + (room_charge * days_stayed) + medicine_cost + other_charges
        return total

    def save(self, *args, **kwargs):
        self.amount = self.calculate_total()
        print(f"Calculated total amount: {self.amount}")  # Debug print statement
        super().save(*args, **kwargs)

    def __str__(self):
      return f"Billing for {self.patient.first_name} {self.patient.last_name}"

