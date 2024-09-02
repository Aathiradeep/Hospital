from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','date_of_birth', 'email', 'phone_number', 'patient_address', 'user', 'doctor']
    search_fields = ['frist_name', 'last_name','email', 'phone_number']  # Optional: To allow searching by these fields
    list_filter = ['doctor', 'date_of_birth']  # Optional: To allow filtering in the admin

    # Optional: Define the fields to be displayed on the admin form for adding/editing patients
    fieldsets = (
        (None, {
            'fields': ('first_name','last_name', 'date_of_birth', 'email', 'phone_number', 'patient_address', 'user', 'doctor', 'medical_history', 'current_medication')
        }),
    )
