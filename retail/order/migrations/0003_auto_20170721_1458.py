# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 02:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pricing', '0002_auto_20170721_1458'),
        ('sale', '0001_initial'),
        ('location', '0001_initial'),
        ('order', '0002_auto_20170721_1458'),
        ('party', '0001_initial'),
        ('customer', '0002_auto_20170721_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.SalesChannel'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Customer'),
        ),
        migrations.AddField(
            model_name='order',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.AbsoluteLocalLocation'),
        ),
        migrations.AddField(
            model_name='order',
            name='price_calculation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.PriceCalculation'),
        ),
        migrations.AddField(
            model_name='order',
            name='price_channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.PriceChannel'),
        ),
        migrations.AddField(
            model_name='order',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.Promotion'),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='party.Organisation'),
        ),
    ]
