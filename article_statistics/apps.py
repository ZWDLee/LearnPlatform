from django.apps import AppConfig


class ArticleStatisticsConfig(AppConfig):
    name = 'article_statistics'

    verbose_name = '课程相关管理'

    # def ready(self):
    #     super(ArticleStatisticsConfig, self).ready()
    #     from . import signals
