# Generated by Django 2.2.3 on 2020-04-25 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_auto_20200420_1642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_time'], 'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
    ]
