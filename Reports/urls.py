# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.report_detail, name='report_detail'),
    # other paths...
]
