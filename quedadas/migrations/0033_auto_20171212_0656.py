# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-12 06:56
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quedadas', '0032_profile_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='challenge',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='friendship',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chat',
            name='lastMessage',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='meeting',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='chatR', to='quedadas.Meeting'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='lastTracking',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quedadas.Tracking'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='maxDistance',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='minDistance',
            field=models.FloatField(default=0),
        ),
    ]