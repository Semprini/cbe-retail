# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-13 23:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('resource', '0001_initial'),
        ('party', '0002_auto_20171214_1248'),
        ('location', '0002_auto_20171214_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(auto_now_add=True)),
                ('valid_to', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('email_contacts', models.ManyToManyField(blank=True, related_name='store_store_email_contacts', to='party.EmailContact')),
                ('individual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Individual')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Location')),
                ('logical_resources', models.ManyToManyField(blank=True, related_name='store_store_logical_resources', to='resource.LogicalResource')),
                ('organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Organisation')),
                ('physical_contacts', models.ManyToManyField(blank=True, related_name='store_store_physical_contacts', to='party.PhysicalContact')),
                ('physical_resources', models.ManyToManyField(blank=True, related_name='store_store_physical_resources', to='resource.PhysicalResource')),
                ('telephone_numbers', models.ManyToManyField(blank=True, related_name='store_store_telephone_numbers', to='party.TelephoneNumber')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
