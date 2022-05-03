from django.urls import path
from . import views

app_name = 'consultation'
urlpatterns = [
    path('', views.consult, name='consult'),
    path('otp/<uid>/', views.otp, name='otp'),
]