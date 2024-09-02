from django.shortcuts import render, redirect
from .forms import TestimonialForm
from .models import Testimonial


def review(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('testimonial')  # Redirect to a page that lists testimonials
    else:
        form = TestimonialForm()
    
    return render(request, 'review_us.html', {'form': form})


def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'testimonial.html', {'testimonials': testimonials})

def submit_review(request):
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        feedback = request.POST.get('feedback')

        # Save the review
        Testimonial.objects.create(
            name=name,
            email=email,
            phone=phone,
            feedback=feedback
        )

        # Redirect to the success page
        return redirect('review_success')

    # If GET request, return review form
    return render(request, 'review_us.html')

def review_success(request):
    return render(request, 'review_success.html')
