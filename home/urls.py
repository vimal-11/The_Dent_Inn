from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('pricing/', views.pricing, name='pricing'),
    path('service/', views.service, name='service'),
    path('appointment/', views.appointment, name='appointment'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('post_testimonial/', views.create_testimonial, name='create_testimonial'),
    path('my_appointments/', views.my_appointments, name='my_appointments'),
    path('cancel-appointment/<id>', views.cancel_appointment, name='cancel_appointments'),
]