# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-07 21:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0004_auto_20170808_0924'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaser',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='saleschannel',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='tendertype',
            options={'ordering': ['id']},
        ),
    ]
