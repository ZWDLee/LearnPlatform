from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from comment.models import Comment
from django.db.models.fields import exceptions


class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    liked_num = models.PositiveIntegerField(default=0, verbose_name='点赞数')

    def __str__(self):
        return '<LikeCount:%s>' % self.liked_num

    def get_comment(self):
        # 此处的一个异常处理,用来捕获没有对象的情况
        # 例如在admin后台中,没有计数值会显示为‘-’
        try:
            comment = Comment.objects.get(pk=self.object_id)
            return comment.text
        # 对象不存在就返回0
        except exceptions.ObjectDoesNotExist:
            return '-'
    get_comment.short_description = '被点赞评论'

    class Meta:
        verbose_name = '点赞统计'
        verbose_name_plural = verbose_name


class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='点赞用户')
    liked_time = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    def __str__(self):
        return '<LikeRecord:%s' % self.user.username

    def get_user_url(self):
        return reverse('user_center', kwargs={'user_center_pk': self.user.pk})

    def get_comment(self):
        # 此处的一个异常处理,用来捕获没有对象的情况
        # 例如在admin后台中,没有计数值会显示为‘-’
        try:
            comment = Comment.objects.get(pk=self.object_id)
            return comment.text
        # 对象不存在就返回'-'
        except exceptions.ObjectDoesNotExist:
            return '-'
    get_comment.short_description = '被点赞评论'

    class Meta:
        verbose_name = '点赞记录'
        verbose_name_plural = verbose_name
