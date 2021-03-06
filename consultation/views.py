from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

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

        # email OTP
        msg_sub = 'OTP for Online Consultation'
        message = f'Your OTP for The Dent Inn online consultaion is {consult_obj.otp}'
        send_mail(
            msg_sub,
            message,
            settings.EMAIL_HOST_USER,
            [consult_obj.email],
        )

        # SMS OTP
        # message_handler = MessageHandler(consult_obj.phone_number, consult_obj.otp)
        # message_handler.send_otp_on_mobile()

        print(consult_obj.phone_number, consult_obj.otp, consult_obj.name, consult_obj.email)
        return redirect('consultation:otp', uid=consult_obj.uid)
    else:
        return render(request, 'consult.html')


def otp(request, uid):
    user = Consultation.objects.get(uid=uid)
    context = {'object': user, 'status': True}
    if request.method == 'POST':
        di1 = request.POST['d1']
        di2 = request.POST['d2']
        di3 = request.POST['d3']
        di4 = request.POST['d4']
        otp = di1 + di2 + di3 + di4
        if otp == user.otp:
            context['status'] = True
            return redirect('consultation:payment', uid=user.uid)
        else:
            user.otp = random.randint(1000, 9999)
            user.save()
            context['status'] = False
            context['fail'] = True
            return render(request, 'otp.html', context)
    return render(request, 'otp.html', context)


def resend_otp(request, uid):
    user = Consultation.objects.get(uid=uid)
    user.otp = random.randint(1000, 9999)
    user.save()

    # email OTP
    msg_sub = 'OTP for Online Consultation'
    message = f'Your OTP for The Dent Inn online consultaion is {user.otp}'
    send_mail(
        msg_sub,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
    )

    # SMS OTP
    # message_handler = MessageHandler(user.phone_number, user.otp)
    # message_handler.send_otp_on_mobile()

    # print(user.phone_number, user.otp, user.name, user.email)
    context = {'object': user, 'resend': True}
    return render(request, 'otp.html', context)


# razorpay client

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def payment(request, uid):
    con_obj = Consultation.objects.get(uid=uid)
    #if request.method == 'POST':
    amount = con_obj.fee
    pay_obj, created = Payment.objects.get_or_create(user=con_obj, 
                                                        total_amount = amount
                                                    )
    pay_obj.save()

    razorpay_order = razorpay_client.order.create({
                                            "amount": int(amount) * 100, 
                                            "currency": "INR", 
                                            "receipt": pay_obj.payment_id,
                                            "payment_capture": "1"
                                            })
    print(razorpay_order['id'])
    pay_obj.razorpay_order_id = razorpay_order['id']
    pay_obj.save()
    callback_url = 'http://'+ str(get_current_site(request))+"/consultation/handlerequest/"
    print("Callback: " + callback_url)

    razorpay_context = {
                        'payment': pay_obj, 
                        'razorpay_order_id': razorpay_order['id'], 
                        'payment_id': pay_obj.payment_id, 
                        'final_price': pay_obj.total_amount, 
                        'razorpay_merchant_id': settings.RAZORPAY_KEY_ID, 
                        'callback_url': callback_url
                        }
    return render(request, 'payment.html', razorpay_context)
    
    #else:
    #   return HttpResponse("404 Not Found") 


@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            raz_payment_id = request.POST.get('razorpay_payment_id', '')
            raz_order_id = request.POST.get('razorpay_order_id','')
            raz_signature = request.POST.get('razorpay_signature','')
            params_dict = { 
            'razorpay_order_id': raz_order_id, 
            'razorpay_payment_id': raz_payment_id,
            'razorpay_signature': raz_signature
            }
            pay_status = None
            
            try:
                pay_db = Payment.objects.get(razorpay_order_id=raz_order_id)
            except:
                pay_status = False
                return render(request, 'paymentstatus.html',{
                                                        # 'id':pay_db.payment_id, 
                                                        'status': pay_status,
                                                        'consultation': True})
            pay_db.razorpay_payment_id = raz_payment_id
            pay_db.razorpay_signature = raz_signature
            pay_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result:
                amount = pay_db.total_amount * 100   #we have to pass in paisa 
                try:
                    #razorpay_client.payment.capture(raz_payment_id, amount)
                    pay_db.Payment_status = 1
                    pay_db.save()
                    con_obj = Consultation.objects.get(uid = pay_db.user.uid)
                    con_obj.is_paid = True
                    con_obj.save()
                    pay_status = True
                    # print(params_dict)
                except Exception as e: 
                    print(e)
                    pay_db.Payment_status = 2
                    pay_db.save()
                    pay_status = False
            else:
                pay_db.Payment_status = 2
                pay_db.save()
                pay_status = False
            return render(request, 'paymentstatus.html',{'id':pay_db.payment_id, 
                                                        'status': pay_status,
                                                        'consultation': True})
        except Exception as e:
            print(e)
            return HttpResponse("404 not found")


def my_consult_booking(request):
    context = {'consultation': True}
    if request.method == 'POST':
        name = request.POST['user-name']
        email = request.POST['user-email']
        phone_number = request.POST['user-phone']

        users = Consultation.objects.filter(email = email, phone_number = phone_number)
        if len(users) < 1:
            #return HttpResponse('No Appointments')
            return render(request, 'my_booking_status.html', {"Nolist": True})
        context['users'] = users
        return render(request, 'my_booking_status.html', context)
    else:
        return render(request, 'my_booking.html', context)