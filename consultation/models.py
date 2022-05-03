from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid
# Create your models here.

class Consultation(models.Model):
    name                = models.CharField(max_length=50)
    phone_number        = PhoneNumberField(null=False, blank=False, unique=True)
    email               = models.EmailField(verbose_name="email", max_length=60)
    symptoms            = models.CharField(max_length=700, null=True)
    otp                 = models.CharField(max_length=100, null=True, blank=True)
    uid                 = models.UUIDField(default=uuid.uuid4)
    meet_link           = models.URLField(null=True)
    registration_time   = models.DateTimeField(auto_now=True)
    fee                 = models.FloatField(null=True, default=250)
    is_paid             = models.BooleanField(default=False)
    is_fixed            = models.BooleanField(default=False)
    is_completed        = models.BooleanField(default=False)



    def __str__(self):
        return self.name