from django.contrib import admin
from .models import Article, ArticleType, ArticleDetail


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'article_type', 'author', 'created_time', 'last_updated_time')


@admin.register(ArticleType)
class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(ArticleDetail)
class ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'num', 'title', 'text', 'created_time', 'last_updated_time')

