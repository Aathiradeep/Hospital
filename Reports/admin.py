# Reports/admin.py
from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'start_date', 'end_date', 'generated_at')
    list_filter = ('report_type', 'generated_at')
    search_fields = ('report_type',)
