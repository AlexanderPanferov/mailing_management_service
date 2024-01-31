from datetime import datetime
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import send_mail
from mailing.models import MailingLog


def send_mailing(mailing):
    now = datetime.now().time()
    if mailing.start_time <= now <= mailing.stop_time:
        for client in mailing.client.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client],
                    fail_silently=False
                )
                log = MailingLog.objects.create(
                    datatime=mailing.start_time,
                    status='successfully',
                    mailing=mailing,
                    client=client.email,
                )
                log.save()


            except SMTPException as error:
                log = MailingLog.objects.create(
                    datatime=mailing.start_time,
                    status='fatally',
                    mailing=mailing,
                    serv_response=error,
                    client=client.email,
                )
                log.save()