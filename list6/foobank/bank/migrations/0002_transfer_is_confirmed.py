# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-09 11:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='completed'),
        ),
    ]
