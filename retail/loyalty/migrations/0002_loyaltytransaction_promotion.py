# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 21:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pricing', '0001_initial'),
        ('loyalty', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loyaltytransaction',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.Promotion'),
        ),
    ]
