from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import ParticipateRecord


@receiver(post_save, sender=ParticipateRecord)
def send_notification(sender, instance, **kwargs):
    recipient = instance.content_object.get_author()
    send_user = instance.user
    if recipient != send_user:
        if instance.content_type.model == 'article':
            verb = '参加了您的课程 《{}》'.format(instance.content_object.title)
        else:
            raise Exception('对象类型错误')
    else:
        return 0
    notification_type = 'participate'
    send_user = instance.user.get_nickname_or_username()
    user_url = instance.get_user_url()
    user_avatar = instance.user.get_user_icon()
    notify.send(
        instance.user,
        recipient=recipient,
        verb=verb,
        send_user=send_user,
        user_url=user_url,
        user_avatar=user_avatar,
        notification_type=notification_type
    )
