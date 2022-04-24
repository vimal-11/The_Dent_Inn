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
]