# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-24 08:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quedadas', '0021_auto_20171115_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatName', models.TextField(unique=True)),
                ('last_message', models.DateTimeField(null=True)),
                ('last_hour', models.CharField(max_length=30)),
                ('friendUsername', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatB', to=settings.AUTH_USER_MODEL)),
                ('userName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatA', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='chat',
            unique_together=set([('userName', 'friendUsername')]),
        ),
    ]