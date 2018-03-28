# Generated by Django 2.0.1 on 2018-03-28 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('human_resources', '0006_auto_20180215_0942'),
        ('supplier_partner', '0003_auto_20180215_0942'),
        ('location', '0002_auto_20180131_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('brand', models.CharField(blank=True, max_length=100)),
                ('sub_brand', models.CharField(blank=True, max_length=100)),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('deleted', 'deleted'), ('exiting', 'exiting'), ('pending', 'pending'), ('suspended', 'suspended')], default='active', max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('tax_code', models.CharField(max_length=50)),
                ('impulse_item', models.BooleanField(default=False)),
                ('key_value_item', models.BooleanField(default=False)),
                ('first_sale_date', models.DateField(blank=True, null=True)),
                ('core_abc', models.BooleanField(default=False)),
                ('core_range', models.BooleanField(default=False)),
                ('range', models.IntegerField(default=0)),
                ('dangerous_classification', models.CharField(blank=True, max_length=50)),
                ('relative_importance_index', models.CharField(blank=True, max_length=10)),
                ('exclusive', models.CharField(blank=True, choices=[('RE', 'Retail Exclusive'), ('E', 'Exclusive'), ('P', 'Proprietary'), ('BTR', 'Better'), ('BES', 'Best'), ('BTY', 'BTY')], max_length=50)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='ProductAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('association_type', models.CharField(choices=[('cross-selling', 'cross-selling'), ('other', 'other')], default='cross-selling', max_length=200)),
                ('rank', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('level', models.CharField(choices=[('division', 'division'), ('category', 'category'), ('department', 'department'), ('sub_department', 'sub_department'), ('fineline', 'fineline')], max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOffering',
            fields=[
                ('sku', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('barcode', models.CharField(blank=True, max_length=50, null=True)),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=200)),
                ('type', models.CharField(choices=[('standard', 'standard'), ('fractional', 'fractional'), ('kit', 'kit')], default='standard', max_length=100)),
                ('unit_of_measure', models.CharField(choices=[('each', 'each'), ('kg', 'kg'), ('meter', 'meter')], default='each', max_length=200)),
                ('retail_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('average_cost_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'ordering': ['sku'],
            },
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colour_name', models.CharField(blank=True, max_length=50, null=True)),
                ('colour_value', models.CharField(blank=True, max_length=50, null=True)),
                ('size_name', models.CharField(blank=True, max_length=50, null=True)),
                ('size_value', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateField(blank=True, null=True)),
                ('unit_of_measure', models.CharField(choices=[('each', 'each'), ('kg', 'kg'), ('meter', 'meter')], default='each', max_length=200)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=8)),
                ('average', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                ('retail_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('reorder_minimum', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductStockTake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('unit_of_measure', models.CharField(choices=[('each', 'each'), ('kg', 'kg'), ('meter', 'meter')], default='each', max_length=200)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=8)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Location')),
                ('product_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_stock_takes', to='product.ProductStock')),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='human_resources.Staff')),
            ],
        ),
        migrations.CreateModel(
            name='SupplierProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_sku', models.CharField(max_length=200)),
                ('barcode', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_of_measure', models.CharField(choices=[('each', 'each'), ('kg', 'kg'), ('meter', 'meter')], default='each', max_length=200)),
                ('carton_quantity', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('cost_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('reccomended_retail_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('reccomended_markup', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('next_available_date', models.DateField(blank=True, null=True)),
                ('quantity_break1', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('quantity_price1', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('quantity_break2', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('quantity_price2', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='supplier_partner.Buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_products', to='product.Product')),
                ('specification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_products', to='product.ProductSpecification')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='supplier_partner.Supplier')),
            ],
            options={
                'ordering': ['supplier_sku'],
            },
        ),
    ]
