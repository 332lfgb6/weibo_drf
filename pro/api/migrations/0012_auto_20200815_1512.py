# Generated by Django 3.0.8 on 2020-08-15 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_common'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='closing_date',
            new_name='closing_time',
        ),
    ]
