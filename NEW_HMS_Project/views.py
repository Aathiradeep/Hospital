from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User,Group
from Doctors.models import Doctor
from Patients.models import Patient
from appointments.models import Appointment
from django.contrib.auth.decorators import login_required



# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST.get('first_name', '')  # Fetch first name if available
        last_name = request.POST.get('last_name', 'Unknown')  # Fetch last name, defaulting to 'Unknown'

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'signup.html')

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create a patient and link to the user
        patient = Patient.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # Add the user to the "Patient" group
        patient_group = Group.objects.get(name='Patient')  # Ensure the group name matches exactly
        user.groups.add(patient_group)

        # Display success message
        messages.success(request, 'Account successfully created! Please log in.')

        # Redirect to login page
        return redirect('login')  # Ensure 'login' matches the URL name for your login view

    return render(request, 'signup.html')

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST.get('user_type')  # Ensure we get the user_type

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Debugging: Check what the user_type and group are
            print(f"User type selected: {user_type}")
            print(f"User groups: {user.groups.all()}")

            # Check if the selected user type matches the user's group
            if user_type == 'Doctor' and user.groups.filter(name='Doctor').exists():
                login(request, user)
                return redirect('doctor_dashboard')
            elif user_type == 'Patient' and user.groups.filter(name='Patient').exists():
                login(request, user)
                return redirect('patient_dashboard')
            elif user_type == 'Admin' and user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Incorrect user type. Please select the correct role.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def custom_logout(request):
    logout(request)  # Logout the user
    messages.success(request, "You have successfully logged out.")
    return redirect('index')  # Redirect to the homepage


# Index view
def index(request):
    return render(request, 'index.html')



# Admin dashboard view
@login_required
def admin_dashboard(request):
    appointments = Appointment.objects.all().order_by('-date')  # Fetch latest appointments
    context = {
        'appointments': appointments,
    }
    return render(request, 'admin_dashboard.html', context)

# Static pages
def about(request):
    return render(request, 'about.html')

def treatment(request):
    return render(request, 'treatment.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def contact(request):
    return render(request, 'contact.html')
