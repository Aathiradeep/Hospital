from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']  # Use fields relevant to the appointment model

        # Optional: Customize widgets for better UI in form fields
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            #'reason': forms.Textarea(attrs={'rows': 3}),
        }
