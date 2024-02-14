from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

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

        subject = 'Status of task %s has been changed' % instance.title
        context = {
            'user': user,
            'subject': subject,
            'message': 'User %s changed status of task from %s to %s.' % (user, instance.previous_status, instance.status),
            'daily': False,
        }
        message = render_to_string('mail/notification_detail.html', context=context)

        recipients_emails = set()
        for user in instance.participants.all():
            if user.email:
                recipients_emails.add(user.email)

        if recipients_emails:
            send_email_notifications.delay(subject, message, list(recipients_emails))
