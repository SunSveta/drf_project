from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import hashlib
import requests

from newpro.models import Subscription, PaymentInfo


@shared_task
def course_update_check(course_pk):

    data_subscription = Subscription.objects.filter(course_id=course_pk)
    for item in data_subscription:
        send_mail(
            subject="Course updating",
            message="We done something with course: {course_pk}!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[item.user_id.email],
            fail_silently=False

        )
        #print(f'done {item.user_id.email}')


def payment_status_check():
    data = PaymentInfo.objects.filter(Status='NEW')
    if data.exists():
        for item in data:
            token = hashlib.sha256(f"{settings.TERMINAL_PASSWORD}{item.PaymentId}{settings.TERMINAL_KEY}".encode())
            token = token.hexdigest()

            request_data = {
                "TerminalKey": settings.TERMINAL_KEY,
                "PaymentId": item.PaymentId,
                "Token": token
            }
            response = requests.post('https://securepay.tinkoff.ru/v2/GetState', json=request_data)

            item.Status = response.json().get('Status')
            item.save()
