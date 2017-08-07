# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-07 21:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0001_initial'),
        ('human_resources', '0004_auto_20170807_1705'),
        ('sale', '0002_auto_20170804_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchaser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(auto_now_add=True)),
                ('valid_to', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('identification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='human_resources.Identification')),
                ('individual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Individual')),
                ('organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Organisation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='sale',
            name='purchaser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sale.Purchaser'),
        ),
    ]
