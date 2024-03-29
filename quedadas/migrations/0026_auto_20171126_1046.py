# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-26 10:46
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quedadas', '0025_auto_20171124_1948'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField(default=0)),
                ('steps', models.IntegerField(default=0)),
                ('totalTimeMillis', models.IntegerField(default=0)),
                ('calories', models.FloatField(default=0)),
                ('meetingsCompletats', models.IntegerField(default=0)),
                ('lastTracking',
                 models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='quedadas.Tracking')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='statistics',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='prof', to='quedadas.Statistics'),
        ),
    ]
