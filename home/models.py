from email import message
from email.policy import default
from django.db import models
from django.forms import BooleanField
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Appointments(models.Model):
    patient_name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name="email", max_length=60)
    contact_no = PhoneNumberField(null=False, blank=False)
    treatment = models.CharField(max_length=100) #must be changes to options
    date = models.DateField(null=True)
    time_slot = models.TimeField(null=True)
    is_active = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    date_time_fixed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.patient_name


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name="email", max_length=60)
    contact_no = PhoneNumberField(null=False, blank=False)
    message = models.TextField()
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name="email", max_length=60)
    subject = models.CharField(max_length=500)
    message = models.TextField()
    is_replied = models.BooleanField(default=False)

    def __str__(self):
        return self.name