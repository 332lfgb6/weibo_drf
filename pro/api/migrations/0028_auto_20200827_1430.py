# Generated by Django 3.0.8 on 2020-08-27 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_remove_group_user_vt_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weibo',
            name='f',
            field=models.CharField(default='微博 HTML5 版', max_length=32),
        ),
    ]
