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
    user = Consultation.objects.get(uid=uid)
    context = {'object': user}
    if request.method == 'POST':
        di1 = request.POST['d1']
        di2 = request.POST['d2']
        di3 = request.POST['d3']
        di4 = request.POST['d4']
        otp = di1 + di2 + di3 + di4
        if otp == user.otp:
            return HttpResponse("success")
        else:
            return HttpResponse("Fail")
    return render(request, 'otp.html', context)