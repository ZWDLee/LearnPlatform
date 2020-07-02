from django.db import models
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from article.models import Article
from django.db.models.fields import exceptions


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(max_length=512, verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论用户')

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE, verbose_name='评论根对象')
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE, verbose_name='评论对象')
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE, verbose_name='回复对象')

    def __str__(self):
        return self.text

    def get_user(self):
        return self.user

    def get_user_url(self):
        return reverse('user_center', kwargs={'user_center_pk': self.user.pk})

    def get_notification_url(self):
        return reverse('article_detail', kwargs={'article_pk': self.pk})

    def get_article(self):
        # 此处的一个异常处理,用来捕获没有对象的情况
        # 例如在admin后台中,没有计数值会显示为‘-’
        try:
            article = Article.objects.get(id=self.object_id)
            return article.title
        # 对象不存在就返回0
        except exceptions.ObjectDoesNotExist:
            return '-'
    get_article.short_description = '课程'

    class Meta:
        verbose_name = '评论'
        ordering = ['comment_time']
        verbose_name_plural = verbose_name


