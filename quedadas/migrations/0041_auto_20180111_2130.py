# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-11 21:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quedadas', '0040_auto_20180111_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ban_count',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
