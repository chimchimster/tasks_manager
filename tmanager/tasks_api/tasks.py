import datetime
import os

from celery import shared_task
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string

from .models import Task


@shared_task
def send_email_notifications(
        subject: str,
        message: str,
        recipients: list[str],
):

    send_mail(
        subject=subject,
        message=subject,
        html_message=message,
        from_email=os.getenv('EMAIL_USER'),
        recipient_list=recipients,
        fail_silently=False,
    )


@shared_task(name='send_daily_project_notification')
def send_daily_project_notification():

    allowed_statuses = ['in_progress', 'to_do']

    cur_date = datetime.datetime.now()
    formatted_date = cur_date.strftime('%Y-%m-%d')

    tasks = Task.objects.filter(status__status__in=allowed_statuses, due_to__lte=formatted_date)

    emails = []
    for task in tasks:
        recipients = [user.email for user in task.participants.all()]

        subject = 'Notification! Status of task %s is %s' % (tasks.title, task.status.status)
        message = 'Good morning! Here is a notification of current status of task %s.' % tasks.title
        context = {
            'subject': subject,
            'message': message,
            'daily': True,
        }
        html_message = render_to_string('mail/notification_detail.html', context=context)
        data_list = [subject, html_message, os.getenv('EMAIL_USER'), recipients]
        emails.append(data_list)

    send_mass_mail(tuple(emails), fail_silently=False)
