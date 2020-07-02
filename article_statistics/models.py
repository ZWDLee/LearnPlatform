
from django.db import models
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import reverse
from django.utils import timezone
from article.models import Article
from django.db.models.fields import exceptions


class ParticipateCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    participate_num = models.IntegerField(default=0, verbose_name='参加人数统计')

    def __str__(self):
        return '%s' % self.participate_num

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
        verbose_name = '参加统计'
        verbose_name_plural = verbose_name


class ParticipateRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    participate = models.BooleanField(default=1, verbose_name='参加状态')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='参加用户')
    participate_time = models.DateField(default=timezone.now, verbose_name='参加时间')

    def __str__(self):
        return '%s' % self.object_id

    def get_user_url(self):
        return reverse('user_center', kwargs={'user_center_pk': self.user.pk})

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
        verbose_name = '参加记录'
        verbose_name_plural = verbose_name


class ParticipateArticleExpandMethod():
    def get_participate_num(self):
        try:
            print(self)
            content_type = ContentType.objects.get_for_model(self)
            participate_num = ParticipateCount.objects.get(
                content_type=content_type, object_id=self.pk).participate_num
            return participate_num
        except exceptions.ObjectDoesNotExist:
            return 0

    get_participate_num.short_description = '参与人数'


class IndexWheels(models.Model):
    img = models.ImageField(upload_to='media/indexwheels/')
    name = models.CharField(max_length=64)
    trackid = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

