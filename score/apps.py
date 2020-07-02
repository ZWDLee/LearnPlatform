from django.apps import AppConfig


class ScoreConfig(AppConfig):
    name = 'score'
    verbose_name = '评分'

    def ready(self):
        super(ScoreConfig, self).ready()
        from . import signals
