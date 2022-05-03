from django.http import HttpResponse
from django.shortcuts import redirect, render

from consultation.models import Consultation
from .mixins import  MessageHandler

import random

# Create your views here.

def consult(request):
    if request.method == 'POST':
        name = request.POST['patient-name']
        ph_no = request.POST['contact-no']
        email = request.POST['patient-email']
        symptoms = request.POST['symptoms']

        #db object creation
        consult_obj = Consultation.objects.create(name = name,
                                                  phone_number = ph_no,
                                                  email = email,
                                                  symptoms = symptoms    
                                                )
        consult_obj.otp = random.randint(1000, 9999)
        consult_obj.save()

        con_obj = Consultation.objects.get(name=name, phone_number=ph_no)
        print(con_obj.phone_number, con_obj.otp, con_obj.name, con_obj.email)

        #message_handler = MessageHandler(con_obj.phone_number, con_obj.otp)
        return redirect('consultation:otp', uid=con_obj.uid)
        
    else:
        return render(request, 'consult.html')

def otp(request, uid):
    if request.method == 'POST':
        otp = request.POST['otp']
        user = Consultation.objects.get(uid=uid)
        if otp == user.otp:
            return HttpResponse("success")
        else:
            return HttpResponse("Fail")
    return HttpResponse("hello")