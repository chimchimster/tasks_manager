from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task, TaskHistory
from .tasks import send_email_notifications


@receiver(post_save, sender=Task)
def update_task_history(sender, instance, created, **kwargs):

    user = kwargs.get('user')

    if not created:
        TaskHistory.objects.create(
            user=user,
            task=instance,
            previous_status=instance.previous_status,
            current_status=instance.status,
        )
        message = 'User %s changed status of task from %s to %s.' % (user, instance.previous_status, instance.status)
        subject = 'Status of task %s has been changed' % instance.title
        recipients_emails = set()
        for user in instance.participants.all():
            if user.email:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                )
                recipients_emails.add(email)

        if recipients_emails:
            send_email_notifications.delay(*recipients_emails)
