# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-13 05:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0005_saleitem_cost_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sale',
            options={'ordering': ['-datetime']},
        ),
    ]
