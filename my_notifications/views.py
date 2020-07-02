from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from .models import SystemNotification


@login_required
def my_notifications(request):
    context = {}
    all_notification = Notification.objects.filter(recipient=request.user, unread=True)
    comment_notification_num = 0
    likes_notification_num = 0
    score_notification_num = 0
    system_notification_num = 0
    for i in range(len(all_notification)):
        if all_notification[i].data['notification_type'] == 'comment' or all_notification[i].data['notification_type'] =='reply':
            comment_notification_num += 1
        if all_notification[i].data['notification_type'] == 'likes':
            likes_notification_num += 1
        if all_notification[i].data['notification_type'] == 'score':
            score_notification_num += 1
        if all_notification[i].data['notification_type'] == 'system':
            system_notification_num += 1
    context['comment_notification_num'] = comment_notification_num
    context['likes_notification_num'] = likes_notification_num
    context['score_notification_num'] = score_notification_num
    context['system_notification_num'] = system_notification_num
    return render(request, 'my_notifications/my_notifications.html', context)


def notification_read(request):
    data = {}
    notification_type = request.GET.get('notification_type', '')
    notification_reply = None
    if notification_type == '评论回复':
        notification_type = 'comment'
        notification_reply = 'reply'
    if notification_type == '收到的赞':
        notification_type = 'likes'
    if notification_type == '收到评价':
        notification_type = 'score'
    if notification_type == '系统消息':
        notification_type = 'system'
    user = request.user
    if user.is_authenticated:
        all_notification = Notification.objects.filter(recipient=user, unread=True)
        notification_count = all_notification.count()
        for i in range(len(all_notification)):
            if all_notification[i].data['notification_type'] == notification_type or \
                    all_notification[i].data['notification_type'] == notification_reply:
                all_notification[i].unread = False
                all_notification[i].save()
                notification_count -= 1
                data['state'] = 'SUCCESS'
    else:
        data['state'] = 'ERROR'
        notification_count = 0
        data['message'] = '请登录'
    data['notification_count'] = notification_count
    return JsonResponse(data)


@login_required
def system_notification(request, notification_id):
    notification = get_object_or_404(SystemNotification, pk=notification_id)
    context = {}
    context['notification'] = notification
    return render(request, 'my_notifications/system_notification.html', context)


@login_required
def delete_notifications(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('my_notifications'))
