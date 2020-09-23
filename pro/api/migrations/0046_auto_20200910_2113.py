# Generated by Django 3.0.8 on 2020-09-10 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_remove_weibo_user_agree_weibo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weibo',
            name='user_agree_weibo_2',
        ),
        migrations.AddField(
            model_name='weibo',
            name='user_agree_weibo',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_agree_weibo_set', through='api.UserAgreeWeibo', to='api.User'),
        ),
    ]
