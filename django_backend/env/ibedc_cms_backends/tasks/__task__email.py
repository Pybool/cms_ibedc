from mails.mailservice import Mailservice
from celery import shared_task 
# from celery.decorators import task
from django.core.mail import send_mail
from time import sleep
from django.db import transaction
# from .models import Promotion

from datetime import datetime
from decimal import Decimal
from math import ceil
import time


@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@shared_task
def send_outward_mail(mail_parameters):
    Mailservice.send_outwards_mail(mail_parameters)
    return True


