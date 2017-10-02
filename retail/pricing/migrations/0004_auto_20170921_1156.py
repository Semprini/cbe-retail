# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-20 23:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20170908_1057'),
        ('customer', '0004_auto_20170824_1650'),
        ('store', '0001_initial'),
        ('pricing', '0003_auto_20170907_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productofferingprice',
            name='mode',
        ),
        migrations.RemoveField(
            model_name='productofferingprice',
            name='mode_amount',
        ),
        migrations.AddField(
            model_name='pricecalculation',
            name='accounts',
            field=models.ManyToManyField(blank=True, to='customer.CustomerAccount'),
        ),
        migrations.AddField(
            model_name='pricecalculation',
            name='categories',
            field=models.ManyToManyField(blank=True, to='product.ProductCategory'),
        ),
        migrations.AddField(
            model_name='pricecalculation',
            name='customers',
            field=models.ManyToManyField(blank=True, to='customer.Customer'),
        ),
        migrations.AddField(
            model_name='pricecalculation',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='pricecalculation',
            name='mode',
            field=models.CharField(choices=[('cost plus', 'cost plus'), ('retail minus', 'retail minus'), ('fixed', 'fixed')], default='retail minus', max_length=200),
        ),
        migrations.AddField(
            model_name='pricecalculation',
            name='mode_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='pricecalculation',
            name='product_offerings',
            field=models.ManyToManyField(blank=True, to='product.ProductOffering'),
        ),
        migrations.AddField(
            model_name='pricecalculation',
            name='stores',
            field=models.ManyToManyField(blank=True, to='store.Store'),
        ),
        migrations.AddField(
            model_name='pricecalculation',
            name='valid_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pricecalculation',
            name='valid_to',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='price_channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.PriceChannel'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='stores',
            field=models.ManyToManyField(blank=True, to='store.Store'),
        ),
    ]