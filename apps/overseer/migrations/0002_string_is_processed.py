# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overseer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='string',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
    ]