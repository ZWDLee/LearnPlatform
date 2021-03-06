# Generated by Django 2.2.3 on 2020-04-20 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article_statistics', '0005_auto_20200316_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participatecount',
            name='participate_num',
            field=models.IntegerField(default=0, verbose_name='参加人数统计'),
        ),
        migrations.AlterField(
            model_name='participaterecord',
            name='participate',
            field=models.BooleanField(default=1, verbose_name='参加状态'),
        ),
        migrations.AlterField(
            model_name='participaterecord',
            name='participate_time',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='参加时间'),
        ),
        migrations.AlterField(
            model_name='participaterecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='参加用户'),
        ),
    ]
