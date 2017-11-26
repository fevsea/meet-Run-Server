# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-26 12:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quedadas', '0026_auto_20171126_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('challenged', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenged', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenge_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
