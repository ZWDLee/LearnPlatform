# Generated by Django 2.2.3 on 2020-04-25 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20200420_1642'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IndexWheels',
        ),
        migrations.AlterField(
            model_name='article',
            name='icon',
            field=models.ImageField(blank=True, default='default/course.jpg', null=True, upload_to='media/uploads/article', verbose_name='课程封面'),
        ),
    ]
