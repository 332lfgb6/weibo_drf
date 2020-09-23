# Generated by Django 3.0.8 on 2020-09-14 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_remove_user_user_vt_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_set_object', to='api.User')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_set_subject', to='api.User')),
            ],
        ),
        migrations.DeleteModel(
            name='UserVtUser',
        ),
    ]