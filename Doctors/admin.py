from django.contrib import admin
from .models import Department, Doctor

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'department', 'email', 'phone_number', 'experience','working_hours_start','working_hours_end']
