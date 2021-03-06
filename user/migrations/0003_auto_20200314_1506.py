# Generated by Django 2.2.3 on 2020-03-14 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200311_1658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='introduction',
            new_name='profile_introduction',
        ),
        migrations.AlterField(
            model_name='profile',
            name='icon',
            field=models.ImageField(blank=True, default='default/头像.svg', null=True, upload_to='media/usericon/'),
        ),
    ]
