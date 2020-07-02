from django import template
from notifications.models import Notification

register = template.Library()


@register.simple_tag
def get_comment_notifications(user):
    all_notification = Notification.objects.filter(recipient=user, unread=True)
    comment_notification_num = 0
    for i in range(len(all_notification)):
        if all_notification[i].data['notification_type'] == 'comment' or all_notification[i].data['notification_type'] == 'reply':
            comment_notification_num += 1
    if comment_notification_num != 0:
        return comment_notification_num
    else:
        return ''


@register.simple_tag
def get_like_notifications(user):
    all_notification = Notification.objects.filter(recipient=user, unread=True)
    likes_notification_num = 0
    for i in range(len(all_notification)):
        if all_notification[i].data['notification_type'] == 'likes':
            likes_notification_num += 1
    if likes_notification_num != 0:
        return likes_notification_num
    else:
        return ''


@register.simple_tag
def get_score_notifications(user):
    all_notification = Notification.objects.filter(recipient=user, unread=True)
    score_notification_num = 0
    for i in range(len(all_notification)):
        if all_notification[i].data['notification_type'] == 'score':
            score_notification_num += 1
    if score_notification_num != 0:
        return score_notification_num
    else:
        return ''


@register.simple_tag
def get_system_notifications(user):
    all_notification = Notification.objects.filter(recipient=user, unread=True)
    system_notification_num = 0
    for i in range(len(all_notification)):
        if all_notification[i].data['notification_type'] == 'system':
            system_notification_num += 1
    if system_notification_num != 0:
        return system_notification_num
    else:
        return ''

