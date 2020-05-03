from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.fields import exceptions


class ArticleType(models.Model):
    type_name = models.CharField(max_length=15, verbose_name='课程类型')

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '课程类型'
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    num = models.PositiveIntegerField(default=1, verbose_name='课时')
    title = models.CharField(max_length=50, verbose_name='课时标题')
    text = RichTextUploadingField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_updated_time = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    def __str__(self):
        return self.title

    def get_notification_url(self):
        return reverse('article_text', kwargs={'article_text_pk': self.pk})

    def get_user_url(self):
        return reverse('user_center', kwargs={'user_center_pk': self.content_object.author.pk})

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
        ordering = ['created_time']
        verbose_name = '课程内容'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='课程标题')
    icon = models.ImageField(
        upload_to='media/uploads/article',
        null=True, blank=True, default='default/course.jpg', verbose_name='课程封面')
    article_type = models.ForeignKey(ArticleType, on_delete=models.CASCADE, verbose_name='课程类型')
    GRADE = {
        (0, '初级'),
        (1, '中级'),
        (2, '高级')
    }
    grade = models.IntegerField(choices=GRADE, default=0, verbose_name='难度等级')
    content = RichTextUploadingField(verbose_name='课程介绍')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    introduction = models.CharField(max_length=100, null=True, blank=True, verbose_name='额外说明')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return "课程：%s" % self.title

    def get_author(self):
        return self.author

    def get_user_url(self):
        return reverse('user_center', kwargs={'user_center_pk': self.author.pk})

    def get_notification_url(self):
        return reverse('article_detail', kwargs={'article_pk': self.pk})

    def get_course_num(self):
        try:
            content_type = ContentType.objects.get_for_model(Article)
            course_num = ArticleDetail.objects.filter(content_type=content_type, object_id=self.pk).count()
            return course_num
        except exceptions.ObjectDoesNotExist:
            return 0

    class Meta:
        ordering = ['-created_time']
        verbose_name = '课程'
        verbose_name_plural = verbose_name

