# Generated by Django 2.2.3 on 2020-04-25 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20200425_1142'),
        ('article_statistics', '0006_auto_20200420_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexWheels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='media/indexwheels/')),
                ('name', models.CharField(max_length=64)),
                ('trackid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
            },
        ),
    ]