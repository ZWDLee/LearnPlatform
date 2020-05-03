from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils.html import strip_tags
from notifications.signals import notify
from .models import Comment


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    if instance.reply_to is None:
        recipient = instance.content_object.content_object.get_author()
        author = instance.get_user()
        if recipient != author:
            # 评论
            content_type_1 = ContentType.objects.get_for_model(instance.content_object.content_object)
            content_type_2 = ContentType.objects.get(model='article')
            if content_type_1 == content_type_2:
                verb = '评论了你的课程'
                about_comment = ''
                notification_type = 'comment'
                jump_url = instance.content_object.get_notification_url() + '?comment_pk=' + str(instance.pk)
            else:
                raise Exception('未知的课程信息')
        else:
            return 0
    else:
        recipient = instance.reply_to
        comment_by = instance.user
        if recipient != comment_by:
            verb = '回复了你的评论'
            about_comment = strip_tags(instance.parent.text)
            notification_type = 'reply'
            jump_url = instance.content_object.get_notification_url() + '?comment_pk=' + str(instance.root.pk)
        else:
            return 0
    reply_text = strip_tags(instance.text)
    article_title = instance.content_object.content_object.title
    send_user = instance.user.get_nickname_or_username()
    user_url = instance.get_user_url()
    user_avatar = instance.user.get_user_icon()
    notify.send(instance.user, recipient=recipient,
                verb=verb,
                action_object=instance,
                send_user=send_user,
                jump_url=jump_url,
                user_url=user_url,
                user_avatar=user_avatar,
                notification_type=notification_type,
                reply_text=reply_text,
                about_comment=about_comment,
                article_title=article_title
                )

