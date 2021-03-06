# Generated by Django 2.0.1 on 2018-03-28 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PriceCalculation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('mode', models.CharField(choices=[('cost plus', 'cost plus'), ('retail minus', 'retail minus'), ('fixed', 'fixed')], default='retail minus', max_length=200)),
                ('mode_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PriceChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOfferingPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('taxable', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
    ]
