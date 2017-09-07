# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-07 03:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('order_type', models.CharField(choices=[('order', 'order'), ('quote', 'quote'), ('estimate', 'estimate')], default='order', max_length=200)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount_excl', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_tax', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=10)),
                ('unit_of_measure', models.CharField(choices=[('each', 'each'), ('kg', 'kg'), ('metre', 'metre')], default='each', max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='order.Order')),
            ],
            bases=('order.order',),
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('order_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='order.Order')),
            ],
            bases=('order.order',),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.Order'),
        ),
    ]
