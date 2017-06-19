# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-19 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20170620_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='supplier_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
