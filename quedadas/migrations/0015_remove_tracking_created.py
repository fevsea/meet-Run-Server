# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-14 10:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('quedadas', '0014_auto_20171114_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tracking',
            name='created',
        ),
    ]
