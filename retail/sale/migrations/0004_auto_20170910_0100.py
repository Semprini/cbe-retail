# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-09 13:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0003_auto_20170907_1652'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='seller',
            new_name='vendor',
        ),
    ]