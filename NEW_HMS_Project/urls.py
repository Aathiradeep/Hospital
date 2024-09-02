"""
URL configuration for NEW_HMS_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views  
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),  # Admin panel at /admin/
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('about/', views.about, name='about'),
    path('treatment/', views.treatment, name='treatment'),
    path('testimonials/', views.testimonial, name='testimonial'),
    path('contact/', views.contact, name='contact'),

    # Include the app-specific URLs
    path('doctors/', include('Doctors.urls')),  # Doctors app
    path('patients/', include('Patients.urls')),  # Patients app
    path('appointments/', include('appointments.urls')),  # Appointments app
    path('reports/', include('Reports.urls')),  # include reports url
    path('billing/', include('Billing.urls')),    
    path('review/', include('Review.urls')), #Review app url

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
