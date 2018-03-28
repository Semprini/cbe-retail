# Generated by Django 2.0.1 on 2018-03-28 01:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pricing', '0002_auto_20180328_1457'),
        ('human_resources', '0006_auto_20180215_0942'),
        ('customer', '0005_auto_20180215_0942'),
        ('product', '0001_initial'),
        ('job_management', '0001_initial'),
        ('credit', '0002_auto_20180131_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchaser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('valid_to', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('basket', 'basket'), ('complete', 'complete')], default='complete', max_length=200)),
                ('docket_number', models.IntegerField()),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_amount_excl', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_tax', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.CustomerAccount')),
            ],
            options={
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=10)),
                ('unit_of_measure', models.CharField(choices=[('each', 'each'), ('kg', 'kg'), ('square metre', 'square metre'), ('lineal metre', 'metre')], default='each', max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cost_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('price_calculation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.PriceCalculation')),
                ('price_channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.PriceChannel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
                ('product_offering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductOffering')),
                ('product_offering_price', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.ProductOfferingPrice')),
                ('promotion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.Promotion')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_items', to='sale.Sale')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SalesChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Tender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenders', to='sale.Sale')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TenderType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='tender',
            name='tender_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.TenderType'),
        ),
        migrations.AddField(
            model_name='sale',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.SalesChannel'),
        ),
        migrations.AddField(
            model_name='sale',
            name='credit_balance_events',
            field=models.ManyToManyField(blank=True, to='credit.CreditBalanceEvent'),
        ),
        migrations.AddField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Customer'),
        ),
        migrations.AddField(
            model_name='sale',
            name='identification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='human_resources.Identification'),
        ),
        migrations.AddField(
            model_name='sale',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='job_management.Job'),
        ),
        migrations.AddField(
            model_name='sale',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pricing.Promotion'),
        ),
        migrations.AddField(
            model_name='sale',
            name='purchaser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sale.Purchaser'),
        ),
        migrations.AddField(
            model_name='sale',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='human_resources.Staff'),
        ),
    ]
