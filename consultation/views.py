from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site

from consultation.models import Consultation, Payment
from .mixins import  MessageHandler

import razorpay
import random

# Create your views here.

def consult(request):
    if request.method == 'POST':
        name = request.POST['patient-name']
        ph_no = request.POST['contact-no']
        email = request.POST['patient-email']
        symptoms = request.POST['symptoms']


        consult_obj, created = Consultation.objects.get_or_create(name = name,
                                                                phone_number = ph_no,
                                                                email = email,    
                                                            )
        consult_obj.symptoms = symptoms
        consult_obj.otp = random.randint(1000, 9999)
        consult_obj.save()

        print(consult_obj.phone_number, consult_obj.otp, consult_obj.name, consult_obj.email)

        #message_handler = MessageHandler(con_obj.phone_number, con_obj.otp)
        return redirect('consultation:otp', uid=consult_obj.uid)

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

def payment(request, uid):
    con_obj = Consultation.objects.get(uid=uid)
    if request.method == 'POST':
        amount = con_obj.fee
        pay_obj, created = Payment.objects.get_or_create(user=con_obj, 
                                                         total_amount = amount
                                                        )
        pay_obj.save()

        # razorpay client

        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = razorpay_client.order.create({
                                                "amount": int(amount) * 100, 
                                                "currency": "INR", 
                                                "receipt": pay_obj.payment_id,
                                                "payment_capture": "1"
                                                })
        print(razorpay_order['id'])
        pay_obj.razorpay_order_id = razorpay_order['id']
        pay_obj.save()
        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
        print(callback_url)

        razorpay_context = {
                            'payment': pay_obj, 
                            'razorpay_order_id': razorpay_order['id'], 
                            'payment_id': pay_obj.payment_id, 
                            'final_price': pay_obj.total_amount, 
                            'razorpay_merchant_id': settings.RAZORPAY_KEY_ID, 
                            'callback_url': callback_url
                           }
        return render(request, '/payment.html', razorpay_context)
    
    else:
        return HttpResponse("404 Not Found") 

def handlerequest(request):
    pass