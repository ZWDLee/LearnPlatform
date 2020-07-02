import xadmin
from article.models import Article, ArticleDetail, ArticleType


class GlobalSetting(object):
    site_title = '勤学在线'
    site_footer = 'LearnPlatform Online'
    menu_style = 'accordion'


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class ArticleAdmin(object):
    list_display = ['id', 'title', 'author', 'article_type', 'grade', 'created_time', 'last_updated_time']
    search_fields = ['id', 'title', 'author__username', 'grade', 'created_time', 'last_updated_time']
    list_filter = ['author__username', 'article_type', 'grade', 'created_time', 'last_updated_time']
    list_editable = ['title', 'article_type', 'grade']


class ArticleDetailAdmin(object):
    list_display = ['id', 'get_article', 'num',  'title', 'created_time', 'last_updated_time']
    search_fields = ['title', 'created_time', 'last_updated_time']
    list_filter = ['title', 'created_time', 'last_updated_time']
    list_editable = ['num', 'title']


class ArticleTypeAdmin(object):
    list_display = ['id', 'type_name']
    search_fields = ['type_name']
    list_editable = ['type_name']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(ArticleDetail, ArticleDetailAdmin)
xadmin.site.register(ArticleType, ArticleTypeAdmin)
xadmin.site.register(xadmin.views.CommAdminView, GlobalSetting)
# xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)
