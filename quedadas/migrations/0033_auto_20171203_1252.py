# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 12:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quedadas', '0032_profile_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='lastTracking',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quedadas.Tracking'),
        ),
    ]