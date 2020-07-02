from django.apps import AppConfig


class LikesConfig(AppConfig):
    name = 'likes'
    verbose_name = '课程点赞'

    def ready(self):
        super(LikesConfig, self).ready()
        from . import signals
