# Generated by Django 3.0.8 on 2020-08-23 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20200823_0420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weibo',
            name='pub_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weibo',
            name='update_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
