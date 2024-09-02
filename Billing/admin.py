from django.contrib import admin
from .models import Bill  # Import the Bill model

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'amount', 'date_generated', 'other_charges']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__name']
    list_filter = ['date_generated', 'doctor']

    readonly_fields = ['date_generated', 'amount']  # Make 'amount' readonly

    def save_model(self, request, obj, form, change):
        # Ensure amount is recalculated and saved before saving the model
        if not change:  # If the object is being created
            obj.save()  # Calculate and set amount
        super().save_model(request, obj, form, change)

    # Optionally, you can use this if you want to display a computed amount for some reason
    # def display_amount(self, obj):
    #     return obj.calculate_total()  # This calls the calculate_total method from the Bill model
    # display_amount.short_description = 'Amount'
