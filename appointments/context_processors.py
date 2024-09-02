
from appointments.utils import get_dashboard_url

def dashboard_url_context(request):
    dashboard_url = None
    
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Doctor").exists():
            dashboard_url = 'doctor_dashboard'
        elif request.user.groups.filter(name="Patient").exists():
            dashboard_url = 'patient_dashboard'
        elif request.user.is_superuser:
            dashboard_url = 'admin_dashboard'
    
    return {'dashboard_url': dashboard_url}



def base_context(request):
    dashboard_url = None
    
    if request.user.is_authenticated:
        dashboard_url = get_dashboard_url(request.user)
    
    return {'dashboard_url': dashboard_url}
