# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-07 04:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_store'),
        ('pricing', '0002_auto_20170907_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='productofferingprice',
            name='mode_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='productofferingprice',
            name='quote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_offering_prices', to='order.Quote'),
        ),
        migrations.AddField(
            model_name='productofferingprice',
            name='taxable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='productofferingprice',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_offering_prices', to='customer.CustomerAccount'),
        ),
    ]