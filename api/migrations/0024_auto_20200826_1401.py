# Generated by Django 3.0.8 on 2020-08-26 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_uservtuser_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservtuser',
            name='group',
            field=models.ManyToManyField(blank=True, null=True, to='api.Group'),
        ),
    ]