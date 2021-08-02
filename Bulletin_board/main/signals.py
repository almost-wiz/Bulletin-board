from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Response
from Bulletin_board.email_data import default_from_email


@receiver(post_save, sender=Response)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'Hello, {instance.on_publication.author.username}! New response on publication ' \
                  f'"{instance.on_publication.title}"'
        message = f'Author: {instance.sender}\n' \
                  f'Message: {instance.message}'
    else:
        subject = f'Hello, {instance.sender}! Good news for you!'
        message = f'Your response to the publication "{instance.on_publication.title}" ' \
                  f'was accepted by the author "{instance.on_publication.author.username}"'

    send_mail(
        subject=subject,
        message=message,
        from_email=default_from_email,
        recipient_list=[instance.on_publication.author.email, ],
    )
