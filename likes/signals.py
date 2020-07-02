from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from notifications.signals import notify
from .models import LikeRecord


@receiver(post_save, sender=LikeRecord)
def send_notification(sender, instance, **kwargs):
    recipient = instance.content_object.user
    send_user = instance.user
    if recipient != send_user:
        if instance.content_type.model == 'comment':
            verb = ' 给你的评论点了赞'
        else:
            raise Exception('对象类型错误')
    else:
        return 0
    notification_type = 'likes'
    jump_url = instance.content_object.content_object.get_notification_url() + '?comment_pk=' + str(
        instance.content_object.pk if instance.content_object.parent is None else instance.content_object.root.pk)
    send_user = instance.user.get_nickname_or_username()
    user_url = instance.get_user_url()
    user_avatar = instance.user.get_user_icon()
    obj_text = strip_tags(instance.content_object.text)
    notify.send(
        instance.user,
        recipient=recipient,
        verb=verb,
        send_user=send_user,
        user_url=user_url,
        user_avatar=user_avatar,
        jump_url=jump_url,
        notification_type=notification_type,
        obj_text=obj_text
    )
