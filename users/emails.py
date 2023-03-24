import random
from django.core.mail import send_mail

from weathertask import settings
from .models import *


def send_otp_via_email(email):
    subject = 'Your account verification emails'
    otp = random.randint(100000, 999999)
    message = f'your otp is {otp}' 
    from_email = settings.EMAIL_HOST
    send_mail(subject, message, from_email, [email])
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()