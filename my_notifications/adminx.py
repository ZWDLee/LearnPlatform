import xadmin
from .models import SystemNotification


class SystemNotificationAdmin(object):
    list_display = ['id', 'title', 'content', 'sender', 'recipient']
    search_fields = ['id', 'title', 'sender__username', 'recipient']
    list_filter = ['sender__username', 'recipient', 'send_time']


xadmin.site.register(SystemNotification, SystemNotificationAdmin)
