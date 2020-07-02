from django.apps import AppConfig


class MyNotificationsConfig(AppConfig):
    name = 'my_notifications'
    verbose_name = '系统消息'

    def ready(self):
        super(MyNotificationsConfig, self).ready()
        from . import signals