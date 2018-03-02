# Generated by Django 2.0.1 on 2018-02-26 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('loyalty', '0002_loyaltytransaction_promotion'),
        ('sale', '0001_initial'),
        ('party', '0004_auto_20180215_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='loyaltytransaction',
            name='sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loyalty_transactions', to='sale.Sale'),
        ),
        migrations.AddField(
            model_name='loyaltytransaction',
            name='sale_items',
            field=models.ManyToManyField(blank=True, to='sale.SaleItem'),
        ),
        migrations.AddField(
            model_name='loyaltytransaction',
            name='scheme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loyalty.LoyaltyScheme'),
        ),
        migrations.AddField(
            model_name='loyaltytransaction',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='party.Organisation'),
        ),
    ]