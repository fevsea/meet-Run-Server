# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-30 19:58
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quedadas', '0028_auto_20171126_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='lastDateTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='lastMessageUserName',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='listUsersChat',
            field=models.ManyToManyField(related_name='chat', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chat',
            name='meeting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='quedadas.Meeting'),
        ),
        migrations.AddField(
            model_name='chat',
            name='type',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='chat',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='chat',
            name='friendUsername',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='last_hour',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='last_time',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='userName',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='username_message',
        ),
    ]
