# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-24 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quedadas', '0024_chat_username_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='username_message',
            field=models.BooleanField(default=True),
        ),
    ]