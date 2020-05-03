from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from notifications.signals import notify
from .models import SystemNotification


@receiver(post_save, sender=SystemNotification)
def send_notification(sender, instance, **kwargs):
    if instance.recipient == 0:
        recipient_obj = User.objects.filter(is_superuser=False)
    if instance.recipient == 1:
        recipient_obj = User.objects.filter(is_superuser=False, profile__user_type=0)
    if instance.recipient == 2:
        recipient_obj = User.objects.filter(is_superuser=False, profile__user_type=1)
    verb = instance.title
    notification_id = instance.pk
    notification_type = 'system'
    notify.send(instance.sender,
                recipient=recipient_obj,
                verb=verb, notification_id=notification_id,
                notification_type=notification_type
                )
