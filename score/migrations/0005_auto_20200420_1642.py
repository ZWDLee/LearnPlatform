# Generated by Django 2.2.3 on 2020-04-20 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0004_auto_20200326_1903'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scorerecord',
            options={'ordering': ['-id'], 'verbose_name_plural': '评分记录'},
        ),
    ]