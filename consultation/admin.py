from django.contrib import admin
from consultation.models import Consultation

# Register your models here.

class ConsultationAdmin(admin.ModelAdmin):
    list_filter = ['name', 'phone_number']
    list_display = ['name', 'email', 'phone_number']
    search_fields = ['name', 'email', 'phone_number']
    
    class Meta:
        model = Consultation

admin.site.register(Consultation, ConsultationAdmin)