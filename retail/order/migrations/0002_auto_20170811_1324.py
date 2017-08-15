# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-11 01:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('customer', '0002_auto_20170811_1315'),
        ('pricing', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='product_offering',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductOffering'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.Promotion'),
        ),
        migrations.AddField(
            model_name='order',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.CustomerAccount'),
        ),
    ]