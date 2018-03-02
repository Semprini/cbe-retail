# Generated by Django 2.0.1 on 2018-02-26 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forecast', '0002_storeproductsaleweek_product'),
        ('product', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeproductsaleweek',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_product_sales_weekly', to='store.Store'),
        ),
        migrations.AddField(
            model_name='productsaleweek',
            name='merch_week',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_sales_weekly_merch_weeks', to='forecast.MerchWeek'),
        ),
        migrations.AddField(
            model_name='productsaleweek',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_sales_weekly', to='product.Product'),
        ),
        migrations.AddField(
            model_name='productforecast',
            name='merch_week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_forecasts', to='forecast.MerchWeek'),
        ),
        migrations.AddField(
            model_name='productforecast',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_forecasts', to='product.Product'),
        ),
        migrations.AddField(
            model_name='merchdate',
            name='merch_week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merch_dates', to='forecast.MerchWeek'),
        ),
    ]