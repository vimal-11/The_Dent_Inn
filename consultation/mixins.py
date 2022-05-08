from django.conf import settings
from twilio.rest import Client

class MessageHandler:

    phone_number = None
    otp = None

    def __init__(self, phone_number, otp):
        self.phone_number = phone_number
        self.otp = otp

    def send_otp_on_mobile(self):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

        message = client.messages.create(
                                    body = f'Your OTP for The Dent Inn online consultaion is {self.otp}',
                                    from_ = '+1234567890',
                                    to = self.phone_number  
                            )