from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail

from home.models import Appointments
from datetime import datetime
from dateutil import parser

# Create your views here.

def home(request):
    return render(request, 'home.html', {})

def contact(request):
    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message_sub = request.POST['message-sub']
        message = request.POST['message']

        # send mail

        send_mail(
            message_sub,
            message,
            message_email,
            [settings.EMAIL_HOST_USER],
        )

        return render(request, 'contact.html', {'message_name': message_name})

    else: 
        return render(request, 'contact.html', {})

def about(request):
    return render(request, 'about.html', {})

def service(request):
    return render(request, 'service.html', {})

def pricing(request):
    return render(request, 'price.html', {})

def appointment(request):
    if request.method == 'POST':
        treatment = request.POST['treatment']
        contact_no = request.POST['contact-no']
        patient_name = request.POST['patient-name']
        patient_email = request.POST['patient-email']
        date = request.POST['slot-date']
        date_format= datetime.strptime(date, "%m/%d/%Y").strftime('%Y-%m-%d')
        time = request.POST['slot-time']
        slot_time = str(parser.parse(time)).split(' ')[1]

        context = {
            'treatment': treatment,
            'contact_no': contact_no,
            'patient_name': patient_name,
            'patient_email': patient_email,
            'date': date_format,
            'slot_time': slot_time
        }

        #saving db

        appnt = Appointments(
                patient_name = patient_name,
                email = patient_email,
                contact_no = contact_no,
                treatment = treatment,
                date = date_format,
                time_slot = slot_time
        )
        appnt.save()

        return render(request, 'appointment.html', {'patient_name': patient_name})

    else: 
        return render(request, 'appointment.html', {})

def testimonial(request):
    if request.method == 'POST':
        email = request.POST['email']
        return render(request, 'testimonial.html', {'email': email})
    else:
        return render(request, 'testimonial.html', {})