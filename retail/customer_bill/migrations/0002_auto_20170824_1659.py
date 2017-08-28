# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-24 04:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sale', '0001_initial'),
        ('customer_bill', '0001_initial'),
        ('location', '0002_auto_20170811_1315'),
        ('customer', '0004_auto_20170824_1650'),
        ('party', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionbillitem',
            name='sale_events',
            field=models.ManyToManyField(blank=True, to='sale.Sale'),
        ),
        migrations.AddField(
            model_name='servicebillitem',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicebillitems', to='customer_bill.CustomerBill'),
        ),
        migrations.AddField(
            model_name='servicebillitem',
            name='sale_events',
            field=models.ManyToManyField(blank=True, to='sale.Sale'),
        ),
        migrations.AddField(
            model_name='rebatebillitem',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rebatebillitems', to='customer_bill.CustomerBill'),
        ),
        migrations.AddField(
            model_name='rebatebillitem',
            name='sale_events',
            field=models.ManyToManyField(blank=True, to='sale.Sale'),
        ),
        migrations.AddField(
            model_name='jobbillitem',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobbillitems', to='customer_bill.CustomerBill'),
        ),
        migrations.AddField(
            model_name='jobbillitem',
            name='sale_events',
            field=models.ManyToManyField(blank=True, to='sale.Sale'),
        ),
        migrations.AddField(
            model_name='disputebillitem',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disputebillitems', to='customer_bill.CustomerBill'),
        ),
        migrations.AddField(
            model_name='disputebillitem',
            name='sale_events',
            field=models.ManyToManyField(blank=True, to='sale.Sale'),
        ),
        migrations.AddField(
            model_name='customerbillspecification',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.CustomerAccount'),
        ),
        migrations.AddField(
            model_name='customerbillspecification',
            name='billing_cycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_bill.CustomerBillingCycle'),
        ),
        migrations.AddField(
            model_name='customerbillspecification',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Location'),
        ),
        migrations.AddField(
            model_name='customerbillspecification',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Organisation'),
        ),
        migrations.AddField(
            model_name='customerbillingcycle',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.CustomerAccount'),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.CustomerAccount'),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='specification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_bill.CustomerBillSpecification'),
        ),
        migrations.AddField(
            model_name='allocationbillitem',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocationbillitems', to='customer_bill.CustomerBill'),
        ),
        migrations.AddField(
            model_name='allocationbillitem',
            name='sale_events',
            field=models.ManyToManyField(blank=True, to='sale.Sale'),
        ),
        migrations.AddField(
            model_name='adjustmentbillitem',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjustmentbillitems', to='customer_bill.CustomerBill'),
        ),
        migrations.AddField(
            model_name='adjustmentbillitem',
            name='sale_events',
            field=models.ManyToManyField(blank=True, to='sale.Sale'),
        ),
        migrations.AddField(
            model_name='accountbillitem',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountbillitems', to='customer_bill.CustomerBill'),
        ),
        migrations.AddField(
            model_name='accountbillitem',
            name='sale_events',
            field=models.ManyToManyField(blank=True, to='sale.Sale'),
        ),
    ]