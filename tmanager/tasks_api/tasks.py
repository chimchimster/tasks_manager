from django.core.mail import send_mail

from celery import shared_task


@shared_task()
def send_email_notifications(
        subject: str,
        message: str,
        sender: str,
        recipients: list[str],
):

    send_mail(
        subject=subject,
        message=message,
        from_email=sender,
        recipient_list=recipients,
        fail_silently=True
    )
