# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-09 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quedadas', '0037_statistics_challenges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='lastMessageUserName',
            field=models.TextField(blank=True, null=True),
        ),
    ]
