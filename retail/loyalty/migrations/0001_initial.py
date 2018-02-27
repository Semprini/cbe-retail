# Generated by Django 2.0.1 on 2018-02-26 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts_receivable', '0003_customerpayment_vendor'),
        ('human_resources', '0006_auto_20180215_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoyaltyScheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('loyalty_rate', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='LoyaltyTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('loyalty_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('identification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human_resources.Identification')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loyalty_transactions', to='accounts_receivable.CustomerPayment')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
