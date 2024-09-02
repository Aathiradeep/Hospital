from django.urls import path
from . import views


urlpatterns = [
    path('review/', views.review, name='review'),
    path('testimonial/', views.testimonial_list, name='testimonial'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('review/submit_review/', views.submit_review, name='submit_review'),
    path('review/success/', views.review_success, name='review_success'),
]
