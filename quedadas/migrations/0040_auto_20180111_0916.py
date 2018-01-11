# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-11 09:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quedadas', '0039_auto_20180111_0807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='ban_count',
        ),
        migrations.AddField(
            model_name='profile',
            name='ban_count',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
