from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import ScoreRecord


@receiver(post_save, sender=ScoreRecord)
def send_notification(sender, instance, **kwargs):
    recipient = instance.content_object.get_author()
    if recipient != instance.user:
        if instance.content_type.model == 'article':
            verb = ' 给 《{0}》 打分：{1}分'.format(instance.content_object.title, instance.scored_num)
        else:
            raise Exception('对象类型错误')
    else:
        return 0
    notification_type = 'score'
    jump_url = instance.content_object.get_notification_url() + '?score_pk=' + str(instance.pk)
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
        jump_url=jump_url,
        notification_type=notification_type
    )



