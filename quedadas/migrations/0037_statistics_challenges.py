# Generated by Django 2.0 on 2017-12-31 19:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quedadas', '0036_auto_20171231_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='challenges',
            field=models.IntegerField(default=0),
        ),
    ]
