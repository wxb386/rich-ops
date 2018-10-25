# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-25 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='id',
        ),
        migrations.RemoveField(
            model_name='host',
            name='id',
        ),
        migrations.AlterField(
            model_name='group',
            name='group',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='host',
            name='ip',
            field=models.GenericIPAddressField(primary_key=True, serialize=False),
        ),
    ]
