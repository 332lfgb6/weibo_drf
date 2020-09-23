# Generated by Django 3.0.8 on 2020-08-25 04:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20200824_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weibo',
            name='pub_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='weibo',
            name='update_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
