from django.core.mail import send_mass_mail, EmailMessage

from celery import shared_task


@shared_task()
def send_email_notifications(
        mails: set[EmailMessage],
):

    send_mass_mail(*mails, fail_silently=True)
