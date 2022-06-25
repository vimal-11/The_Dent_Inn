from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import uuid


import razorpay
# Create your models here.

class Consultation(models.Model):
    name                = models.CharField(max_length=50)
    phone_number        = PhoneNumberField(null=False, blank=False)
    email               = models.EmailField(verbose_name="email", max_length=60)
    symptoms            = models.CharField(max_length=700, null=True)
    otp                 = models.CharField(max_length=100, null=True, blank=True)
    uid                 = models.UUIDField(default=uuid.uuid4)
    meet_link           = models.URLField(null=True)
    registration_time   = models.DateTimeField(auto_now=True)
    consultation_time   = models.DateTimeField(null=True, blank=True)
    fee                 = models.FloatField(default=250)
    is_paid             = models.BooleanField(default=False)
    is_fixed            = models.BooleanField(default=False)
    is_completed        = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Payment(models.Model):
    Payment_status_choices = (
                            (1, 'SUCCESS'),
                            (2, 'FAILURE'),
                            (3, 'PENDING'),
                    )
    user = models.ForeignKey(Consultation, on_delete=models.RESTRICT)
    total_amount = models.FloatField()
    Payment_status = models.IntegerField(choices=Payment_status_choices, default=3)
    payment_id = models.CharField(unique=True, blank=True, null=True, default=None, max_length=100)
    time_of_payment = models.DateTimeField(default=timezone.now)

    razorpay_order_id = models.CharField(max_length=500, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=500, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.payment_id is None and self.time_of_payment and self.id:
            self.payment_id = self.time_of_payment.strftime('DENT2000RAZ%Y%m%dID') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.name + str(self.user.phone_number) + str(self.id)