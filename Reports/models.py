from django.db import models
from Patients.models import Patient
from Doctors.models import Doctor
from Billing.models import Bill
from django.utils import timezone
from appointments.models import Appointment

class Report(models.Model):
    REPORT_CHOICES = [
        ('PATIENTS', 'Patients Report'),
        ('DOCTORS', 'Doctors Report'),
        ('APPOINTMENTS', 'Appointments Report'),
        ('REVENUE', 'Revenue Report'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.get_report_type_display()} from {self.start_date} to {self.end_date}"

    def total_doctors(self):
        return Doctor.objects.count()

    def total_patients(self):
        return Patient.objects.count()

    def total_appointments(self):
        # Assuming you have an Appointment model
        return Appointment.objects.filter(date__range=[self.start_date, self.end_date]).count()

    def total_revenue(self):
        return Bill.objects.filter(date_generated__range=[self.start_date, self.end_date]).aggregate(total_revenue=models.Sum('amount'))['total_revenue'] or 0

    def generate_report(self):
        # Method to generate and return the report data
        return {
            'total_doctors': self.total_doctors(),
            'total_patients': self.total_patients(),
            'total_appointments': self.total_appointments(),
            'total_revenue': self.total_revenue()
        }
