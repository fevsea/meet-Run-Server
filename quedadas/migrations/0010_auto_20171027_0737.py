# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 07:37
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quedadas', '0009_auto_20171025_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='prof',
                                       to=settings.AUTH_USER_MODEL),
        ),
    ]
