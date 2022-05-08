from django.contrib import admin
from consultation.models import Consultation, Payment

# Register your models here.

class ConsultationAdmin(admin.ModelAdmin):
    list_filter = ['name', 'phone_number']
    list_display = ['name', 'email', 'phone_number']
    search_fields = ['name', 'email', 'phone_number']
    
    class Meta:
        model = Consultation

admin.site.register(Consultation, ConsultationAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_filter = ['user', 'payment_id']
    list_display = ['user', 'time_of_payment', 'payment_id']
    search_fields = ['user', 'total_amount', 'time_of_payment', 'payment_id']
    
    class Meta:
        model = Payment

admin.site.register(Payment, PaymentAdmin)