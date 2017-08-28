# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-27 22:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='owner',
            new_name='organisation',
        ),
        migrations.AddField(
            model_name='store',
            name='individual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Individual'),
        ),
        migrations.AddField(
            model_name='store',
            name='valid_from',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='valid_to',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]