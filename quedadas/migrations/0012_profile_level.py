# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-03 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quedadas', '0011_auto_20171102_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
