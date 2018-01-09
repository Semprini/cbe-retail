# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-09 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20171219_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='dangerous_classification',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='exclusive',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='product',
            name='range',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='relative_importance_index',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_brand',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='supplierproduct',
            name='next_available_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]