# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 02:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0002_auto_20171214_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaser',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
