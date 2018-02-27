# Generated by Django 2.0.1 on 2018-02-26 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MerchDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar_date', models.DateField()),
                ('calendar_date_txt', models.CharField(max_length=100)),
                ('calendar_week_end', models.DateField()),
                ('calendar_week_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MerchWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('calendar_start', models.DateField(blank=True, null=True)),
                ('calendar_end', models.DateField()),
                ('calendar_week_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductForecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.CharField(db_index=True, max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSaleWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateField()),
                ('product_txtid', models.CharField(max_length=50)),
                ('store_count', models.IntegerField()),
                ('quantity', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('on_hand', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('on_order', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('store_stock_count', models.IntegerField()),
                ('store_sales_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StoreProductSaleWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateField()),
                ('product_txtid', models.CharField(max_length=50)),
                ('quantity', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('on_hand', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('on_order', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('retail_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('average_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('merch_week', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_product_sales_weekly_merch_weeks', to='forecast.MerchWeek')),
            ],
        ),
    ]
