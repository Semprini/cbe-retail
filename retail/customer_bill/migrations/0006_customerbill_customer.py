# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-27 22:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.core.exceptions import ObjectDoesNotExist

from cbe.customer.models import Customer

@property
def set_my_defaults():
    try:
        return Customer.objects.first().pk
    except ObjectDoesNotExist:
        return 0

class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20170824_1650'),
        ('customer_bill', '0005_auto_20170828_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='customer',
            field=models.ForeignKey(default=set_my_defaults, on_delete=django.db.models.deletion.CASCADE, to='customer.Customer'),
            preserve_default=False,
        ),
    ]
