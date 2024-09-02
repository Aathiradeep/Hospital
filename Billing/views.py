from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Bill
from django.views.generic import DetailView
from django.urls import reverse
from Patients.models import Patient
from Doctors.models import Doctor
from django.template.loader import get_template
from django.http import JsonResponse,HttpResponse
from decimal import Decimal
from io import BytesIO
from xhtml2pdf import pisa
from datetime import datetime




def generate_bill(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        patient_phone = request.POST.get('patient_phone')
        patient_address = request.POST.get('patient_address')
        room_charge = Decimal(request.POST.get('room_charge') or 0)
        days_stayed = Decimal(request.POST.get('days_stayed') or 0)
        medicine_cost = Decimal(request.POST.get('medicine_cost') or 0)
        other_charges = Decimal(request.POST.get('other_charges') or 0)
        consultation_fee = Decimal(request.POST.get('consultation_fee') or 0)

        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)

        bill = Bill(
            patient=patient,
            doctor=doctor,
            patient_phone=patient_phone,
            patient_address=patient_address,
            room_charge=room_charge,
            days_stayed=days_stayed,
            medicine_cost=medicine_cost,
            other_charges=other_charges,
            consultation_fee=consultation_fee
        )
        bill.save()
        messages.success(request, 'Bill generated successfully.')
        return redirect('doctor_dashboard')  # Ensure this URL name is correct for the doctor dashboard
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'generate_bill.html', {'patients': patients, 'doctors': doctors})

@login_required
def patient_bills(request):
    selected_date = request.GET.get('date')
    user = request.user

    if not hasattr(user, 'patient'):
        return render(request, 'error.html', {'message': 'Patient profile not found.'})

    patient = user.patient
    bills = Bill.objects.none()  # Default to no bills if no date is provided

    if selected_date:
        try:
            # Convert selected_date to a date object
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            
            # Filter bills for the patient on the selected date
            bills = Bill.objects.filter(date_generated__date=selected_date, patient=patient)
        except ValueError:
            # Handle invalid date format
            return render(request, 'error.html', {'message': 'Invalid date format.'})

    context = {
        'bills': bills,
        'selected_date': selected_date
    }
    return render(request, 'patient_bills.html', context)

@login_required
def doctor_bills(request):
    doctor = request.user.doctor
    bills = Bill.objects.filter(doctor=doctor).order_by('-date_generated')
    return render(request, 'doctor_bills.html', {'bills': bills})

@login_required 
def billing_list(request):
    patients = Patient.objects.all()  # Retrieve all patients
    selected_patient_id = request.GET.get('patient')  # Get selected patient ID from the dropdown

    # If a patient is selected, filter bills by that patient, else show all bills
    if selected_patient_id:
        bills = Bill.objects.filter(patient_id=selected_patient_id)
    else:
        bills = Bill.objects.all()  # Default to showing all bills if no patient is selected

    context = {
        'patients': patients,
        'bills': bills,
        'selected_patient_id': selected_patient_id,
    }
    return render(request, 'billing_list.html', context)


@login_required
def billing_detail(request, billing_id):
    billing = get_object_or_404(Bill, id=billing_id)
    return render(request, 'billing_detail.html', {'bill': billing})


@login_required
def download_pdf(request, billing_id):
    billing = get_object_or_404(Bill, id=billing_id)
    template_path = 'billing_pdf_template.html'
    context = {'billing': billing}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{billing_id}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response.write(result.getvalue())
        return response
    
    # Log error for debugging
    error_message = f'PDF generation failed for billing ID {billing_id}. Error: {pdf.err}'
    print(error_message)  # Replace with logging
    return HttpResponse('We had some errors <pre>' + html + '</pre>')



@login_required
   
def get_bill_details(request, patient_name):
    # Split the full_name into first_name and last_name
    name_parts = patient_name.split()
    if len(name_parts) != 2:
        return JsonResponse({'error': 'Invalid patient name format. Please provide both first and last name.'}, status=400)
    
    first_name, last_name = name_parts

    try:
        # Fetch the patient by first and last name
        patient = Patient.objects.get(first_name=first_name, last_name=last_name)
        
        # Fetch bills associated with the patient
        bills = Bill.objects.filter(patient=patient)
        bill_list = [{
            'id': bill.id,
            'doctor': bill.doctor.name,
            'date_generated': bill.date_generated.strftime('%d %b %Y'),
            'amount': str(bill.amount),
            'patient_phone': bill.patient_phone,
            'patient_address': bill.patient_address,
            'room_charge': str(bill.room_charge),
            'medicine_cost': str(bill.medicine_cost),
            'other_charges': str(bill.other_charges),
            'days_stayed': bill.days_stayed,
            'consultation_fee': str(bill.consultation_fee)
        } for bill in bills]
        
        return JsonResponse({'bills': bill_list})
    
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'No patient found with the given name'}, status=404)
    
def get_patient_details(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        data = {
            'phone_number': patient.phone_number,
            'address': patient.patient_address
        }
        return JsonResponse(data)
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)
    
