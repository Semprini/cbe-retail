# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-12 00:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20171222_1536'),
        ('product', '0005_auto_20180111_1406'),
        ('forecast', '0005_productsaleweek_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreProductSaleWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateField()),
                ('quantity', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('on_hand', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('on_order', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('retail_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('average_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('merch_week', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_product_sales_weekly_merch_weeks', to='forecast.MerchWeek')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_product_sales_weekly', to='product.Product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_product_sales_weekly', to='store.Store')),
            ],
        ),
        migrations.RemoveField(
            model_name='productsaleweek',
            name='merch_week',
        ),
        migrations.RemoveField(
            model_name='productsaleweek',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productsaleweek',
            name='store',
        ),
        migrations.DeleteModel(
            name='ProductSaleWeek',
        ),
    ]
