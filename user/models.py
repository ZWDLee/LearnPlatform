from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户账号')
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    icon = models.ImageField(upload_to='media/user_avatar/%Y/%m/%d', null=True, blank=True,
                             default='default/avatar.svg', verbose_name='用户头像')
    GENDER = (
        (0, '男'),
        (1, '女'),
        (2, '保密')
    )
    gender = models.IntegerField(choices=GENDER, default=2, verbose_name='性别')
    birth = models.DateField(null=True, blank=True, verbose_name='出生日期')
    user_type = models.BooleanField(default=False, verbose_name='用户类别')
    EDUCATION = (
        (0, '小学'),
        (1, '初中'),
        (2, '高中'),
        (3, '专科'),
        (4, '本科'),
        (5, '研究生'),
        (6, '硕士'),
        (7, '博士'),
        (8, '其他')
    )
    education = models.IntegerField(default=8, choices=EDUCATION, verbose_name='当前学历')
    introduction = models.CharField(max_length=50, null=True, blank=True, verbose_name='简介')

    def __str__(self):
        return '<Profile:%s for %s>' % (self.nickname, self.user.username)

    class Meta:
        verbose_name = '用户档案'
        verbose_name_plural = verbose_name


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


def get_user_icon(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.icon.url
    else:
        return 0


def get_user_introduction(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        if profile.introduction:
            return profile.introduction
        else:
            return '这个人很懒，什么都没留下！'
    else:
        return '这个人很懒，什么都没留下！'


def get_user_type(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.user_type


User.get_nickname_or_username = get_nickname_or_username
User.get_user_type = get_user_type
User.get_user_introduction = get_user_introduction
User.get_user_icon = get_user_icon
