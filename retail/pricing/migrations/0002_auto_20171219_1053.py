# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 21:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0004_auto_20171214_1743'),
        ('product', '0001_initial'),
        ('pricing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='categories',
            field=models.ManyToManyField(blank=True, to='product.ProductCategory'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='customers',
            field=models.ManyToManyField(blank=True, to='customer.Customer'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='price_channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.PriceChannel'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='product_offerings',
            field=models.ManyToManyField(blank=True, to='product.ProductOffering'),
        ),
    ]