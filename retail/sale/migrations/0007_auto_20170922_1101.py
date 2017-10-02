# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-21 23:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0005_productofferingprice_calculation'),
        ('job_management', '0001_initial'),
        ('sale', '0006_auto_20170913_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='price_calculation',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='price_channel',
        ),
        migrations.AddField(
            model_name='sale',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job_management.Job'),
        ),
        migrations.AddField(
            model_name='sale',
            name='status',
            field=models.CharField(choices=[('basket', 'basket'), ('complete', 'complete')], default='complete', max_length=200),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='price_calculation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.PriceCalculation'),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='price_channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.PriceChannel'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total_amount_excl',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total_tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='product_offering_price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.ProductOfferingPrice'),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='unit_of_measure',
            field=models.CharField(choices=[('each', 'each'), ('kg', 'kg'), ('square metre', 'square metre'), ('lineal metre', 'metre')], default='each', max_length=200),
        ),
    ]