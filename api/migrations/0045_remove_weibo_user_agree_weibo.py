# Generated by Django 3.0.8 on 2020-09-10 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20200910_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weibo',
            name='user_agree_weibo',
        ),
    ]
