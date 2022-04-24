from django.contrib import admin
from home.models import Appointments

# Register your models here.

class AppointmentsAdmin(admin.ModelAdmin):
    list_filter = ['patient_name']
    list_display = ['patient_name', 'email', 'contact_no',]
    search_fields = ['patient_name', 'email', 'contact_no', 'date', 'treatment']
    
    class Meta:
        model = Appointments

admin.site.register(Appointments, AppointmentsAdmin)