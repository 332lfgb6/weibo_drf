# Generated by Django 3.0.8 on 2020-08-26 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_remove_uservtuser_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservtuser',
            name='group',
            field=models.ManyToManyField(to='api.Group'),
        ),
    ]
