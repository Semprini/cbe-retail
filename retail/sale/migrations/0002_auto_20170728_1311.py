# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-28 01:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saleitem',
            old_name='product',
            new_name='product_offering',
        ),
    ]
