# Generated by Django 2.2.3 on 2020-03-15 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_statistics', '0002_auto_20200314_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participatearticle',
            name='participate_num',
            field=models.BooleanField(default=1),
        ),
    ]
