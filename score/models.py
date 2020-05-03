from django.db import models
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from article.models import Article
from django.db.models.fields import exceptions


class ScoreRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    scored_num = models.PositiveIntegerField(default=0, verbose_name='分数')
    text = models.CharField(max_length=100, verbose_name='评价内容')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评价用户')
    scored_time = models.DateField(auto_now_add=True, verbose_name='评分时间')

    def get_user_url(self):
        return reverse('user_center', kwargs={'user_center_pk': self.user.pk})

    def get_article(self):
        try:
            article = Article.objects.get(id=self.object_id)
            return article.title
        # 对象不存在就返回0
        except exceptions.ObjectDoesNotExist:
            return '-'

    get_article.short_description = '课程'

    class Meta:
        ordering = ['-id']
        verbose_name_plural = '评分记录'


class ScoreAverage(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    average = models.FloatField(max_length=2, verbose_name='平均分')
    count = models.IntegerField(default=0, verbose_name='评分条数')

    def get_article(self):
        try:
            article = Article.objects.get(id=self.object_id)
            return article.title
        # 对象不存在就返回0
        except exceptions.ObjectDoesNotExist:
            return '-'

    get_article.short_description = '课程'

    class Meta:
        verbose_name_plural = '评分平均分'
