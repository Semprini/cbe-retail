# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 02:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pricing', '0002_auto_20170721_1458'),
        ('location', '0001_initial'),
        ('resource', '0001_initial'),
        ('human_resources', '0002_auto_20170721_1450'),
        ('product', '0001_initial'),
        ('party', '0001_initial'),
        ('customer', '0002_auto_20170721_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('docket_number', models.CharField(blank=True, max_length=50, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount_excl', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.CustomerAccount')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=10)),
                ('unit_of_measure', models.CharField(choices=[('each', 'each'), ('kg', 'kg'), ('metre', 'metre')], default='each', max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductOffering')),
                ('promotion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.Promotion')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_items', to='sale.Sale')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SalesChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenders', to='sale.Sale')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TenderType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='tender',
            name='tender_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.TenderType'),
        ),
        migrations.AddField(
            model_name='sale',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.SalesChannel'),
        ),
        migrations.AddField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Customer'),
        ),
        migrations.AddField(
            model_name='sale',
            name='identification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='human_resources.Identification'),
        ),
        migrations.AddField(
            model_name='sale',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.AbsoluteLocalLocation'),
        ),
        migrations.AddField(
            model_name='sale',
            name='price_calculation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.PriceCalculation'),
        ),
        migrations.AddField(
            model_name='sale',
            name='price_channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.PriceChannel'),
        ),
        migrations.AddField(
            model_name='sale',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.Promotion'),
        ),
        migrations.AddField(
            model_name='sale',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='party.Organisation'),
        ),
        migrations.AddField(
            model_name='sale',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='human_resources.Staff'),
        ),
        migrations.AddField(
            model_name='sale',
            name='till',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resource.PhysicalResource'),
        ),
    ]
