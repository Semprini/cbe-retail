# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-17 04:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sale',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='saleitem',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='tender',
            options={'ordering': ['id']},
        ),
    ]
