# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 11:33
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quedadas', '0010_auto_20171027_0737'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creator',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_creator_set',
                                   to=settings.AUTH_USER_MODEL)),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_set',
                                             to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='meeting',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
