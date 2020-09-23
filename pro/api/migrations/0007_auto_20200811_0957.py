# Generated by Django 3.0.8 on 2020-08-11 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200810_0443'),
    ]

    operations = [
        migrations.AddField(
            model_name='weibo',
            name='type',
            field=models.CharField(default='文本', max_length=2),
        ),
        migrations.AlterField(
            model_name='weibo',
            name='collection',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_collect_weibo', to='api.User'),
        ),
        migrations.AlterField(
            model_name='weibo',
            name='user_ban_weibo',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_ban_weibo_set', to='api.User'),
        ),
        migrations.AlterField(
            model_name='weiboimg',
            name='uri',
            field=models.ImageField(upload_to='weibo_images'),
        ),
    ]