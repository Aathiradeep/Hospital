from django.contrib import admin
from Doctors.models import Doctor
from Patients.models import Patient
from Billing.models import Bill
from Reports.models import HospitalReport

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Bill)
admin.site.register(HospitalReport)
