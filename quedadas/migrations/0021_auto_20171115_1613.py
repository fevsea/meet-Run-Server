# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-15 16:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quedadas', '0020_auto_20171114_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='tracking',
        ),
        migrations.AddField(
            model_name='tracking',
            name='meeting',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='quedadas.Meeting'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tracking',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]