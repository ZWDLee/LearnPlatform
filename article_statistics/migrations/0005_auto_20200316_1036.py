# Generated by Django 2.2.3 on 2020-03-16 02:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article_statistics', '0004_auto_20200315_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participaterecord',
            name='participate_time',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]