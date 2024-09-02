from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    feedback = models.TextField()

    def __str__(self):
        return self.name

    def summary(self):
        return f"{self.name}: {self.feedback[:100]}..."  # Display a summary of feedback
