# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quedadas', '0002_auto_20171017_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='level',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
