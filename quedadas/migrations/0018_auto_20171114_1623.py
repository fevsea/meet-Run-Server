# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 16:23
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quedadas', '0017_auto_20171114_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routepoint',
            name='order',
        ),
        migrations.AlterField(
            model_name='meeting',
            name='tracking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meeting',
                                    to='quedadas.Tracking'),
        ),
    ]
