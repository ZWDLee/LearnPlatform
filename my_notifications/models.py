from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class SystemNotification(models.Model):
    title = models.CharField(max_length=30, verbose_name='消息标题')
    content = RichTextUploadingField(verbose_name='消息正文')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    RECIPIENT = (
        (0, '全体'),
        (1, '学生'),
        (2, '教师')
    )
    recipient = models.IntegerField(default=0, choices=RECIPIENT)
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '系统消息'
        verbose_name_plural = verbose_name
