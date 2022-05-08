from django.urls import path
from . import views

app_name = 'consultation'
urlpatterns = [
    path('', views.consult, name='consult'),
    path('otp/<uid>/', views.otp, name='otp'),
    path('payment/<uid>', views.payment, name='payment'),
    path('handlerequest/', views.handlerequest, name = 'handlerequest'),
    path('resendotp/<uid>', views.resend_otp, name = 'resendotp'),
]