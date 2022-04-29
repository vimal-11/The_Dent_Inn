from django.contrib import admin
from home.models import Appointments, Testimonial

# Register your models here.

class AppointmentsAdmin(admin.ModelAdmin):
    list_filter = ['patient_name']
    list_display = ['patient_name', 'email', 'contact_no',]
    search_fields = ['patient_name', 'email', 'contact_no', 'date', 'treatment']
    
    class Meta:
        model = Appointments

admin.site.register(Appointments, AppointmentsAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name', 'email', 'contact_no',]
    search_fields = ['name', 'email', 'contact_no']

    class Meta:
        model = Testimonial

admin.site.register(Testimonial, TestimonialAdmin)
