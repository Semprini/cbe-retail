# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-13 23:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('order', '0003_auto_20171214_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store'),
        ),
    ]
