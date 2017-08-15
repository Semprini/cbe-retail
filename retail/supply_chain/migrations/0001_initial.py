# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-12 00:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asn_reference', models.CharField(blank=True, max_length=32, null=True)),
                ('message_date_time', models.DateTimeField(blank=True, null=True)),
                ('message_received_date_time', models.DateTimeField(blank=True, null=True)),
                ('despatch_date_time', models.DateTimeField(blank=True, null=True)),
                ('shipment_due_date_time', models.DateTimeField(blank=True, null=True)),
                ('final_shipment_flag', models.IntegerField(blank=True, null=True)),
                ('purchase_order_reference', models.CharField(blank=True, max_length=10, null=True)),
                ('mitre_10_supplier_code', models.CharField(blank=True, max_length=15, null=True)),
                ('mitre_10_buyer_store_code', models.CharField(blank=True, max_length=10, null=True)),
                ('mitre_10_delivery_store_code', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'asns',
            },
        ),
        migrations.CreateModel(
            name='PoExpectedDeliveryDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_order_reference', models.CharField(blank=True, max_length=15, null=True)),
                ('expected_delivery_date', models.DateTimeField(blank=True, null=True)),
                ('mitre_10_supplier_code', models.CharField(blank=True, max_length=15, null=True)),
                ('message_received_date_time', models.DateTimeField(blank=True, null=True)),
                ('source_record_table', models.CharField(blank=True, max_length=31, null=True)),
                ('source_record_id', models.CharField(blank=True, max_length=50, null=True)),
                ('mitre_10_delivery_store_code', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'db_table': 'po_expected_delivery_date',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderAcknowledgementLineItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_barcode', models.CharField(blank=True, max_length=15, null=True)),
                ('mitre_10_item_code', models.CharField(blank=True, db_column='mitre_10_Item_code', max_length=15, null=True)),
                ('supplier_item_code', models.CharField(blank=True, db_column='supplier_item_Code', max_length=15, null=True)),
                ('item_description', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(blank=True, max_length=6, null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('notification_code', models.IntegerField(blank=True, null=True)),
                ('notification_description', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'purchase_order_acknowledgement_line_items',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderAcknowledgements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poa_reference', models.CharField(blank=True, max_length=32, null=True)),
                ('message_date_time', models.DateTimeField(blank=True, null=True)),
                ('message_received_date_time', models.DateTimeField(blank=True, null=True)),
                ('delivery_date_time_requested', models.DateTimeField(blank=True, null=True)),
                ('delivery_date_time_estimated', models.DateTimeField(blank=True, null=True)),
                ('purchase_order_reference', models.CharField(blank=True, max_length=10, null=True)),
                ('mitre_10_supplier_code', models.CharField(blank=True, max_length=15, null=True)),
                ('mitre_10_buyer_store_code', models.CharField(blank=True, max_length=10, null=True)),
                ('mitre_10_delivery_store_code', models.CharField(blank=True, max_length=10, null=True)),
                ('message_function_code', models.IntegerField(blank=True, null=True)),
                ('message_function_description', models.CharField(blank=True, max_length=50, null=True)),
                ('latest_flag', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'purchase_order_acknowledgements',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderLineItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_barcode', models.CharField(blank=True, max_length=15, null=True)),
                ('mitre_10_item_code', models.CharField(blank=True, max_length=15, null=True)),
                ('supplier_item_code', models.CharField(blank=True, max_length=15, null=True)),
                ('item_description', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(blank=True, max_length=6, null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True)),
                ('conversion_factor', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'purchase_order_line_items',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_order_reference', models.CharField(blank=True, max_length=10, null=True)),
                ('mitre_10_supplier_code', models.CharField(blank=True, max_length=15, null=True)),
                ('mitre_10_buyer_store_code', models.CharField(blank=True, max_length=15, null=True)),
                ('mitre_10_delivery_store_code', models.CharField(blank=True, max_length=15, null=True)),
                ('purchase_order_date', models.DateTimeField(blank=True, null=True)),
                ('despatched_date_time', models.DateTimeField(blank=True, null=True)),
                ('delivery_due_date', models.DateTimeField(blank=True, null=True)),
                ('latest_flag', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'purchase_orders',
            },
        ),
        migrations.CreateModel(
            name='SchemaVersion',
            fields=[
                ('installed_rank', models.IntegerField(primary_key=True, serialize=False)),
                ('version', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=20)),
                ('script', models.CharField(max_length=1000)),
                ('checksum', models.IntegerField(blank=True, null=True)),
                ('installed_by', models.CharField(max_length=100)),
                ('installed_on', models.DateTimeField()),
                ('execution_time', models.IntegerField()),
                ('success', models.IntegerField()),
            ],
            options={
                'db_table': 'schema_version',
            },
        ),
        migrations.CreateModel(
            name='Sscc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sscc_barcode', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('package_type', models.CharField(blank=True, max_length=20, null=True)),
                ('parent_sscc_barcode', models.CharField(blank=True, max_length=20, null=True)),
                ('height_mm', models.FloatField(blank=True, null=True)),
                ('width_mm', models.FloatField(blank=True, null=True)),
                ('weight_kilos', models.FloatField(blank=True, null=True)),
                ('length_mm', models.FloatField(blank=True, null=True)),
                ('asn', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.Asns')),
            ],
            options={
                'db_table': 'sscc',
            },
        ),
        migrations.CreateModel(
            name='SsccAuditCorrectionActions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audit_correction_action_type', models.CharField(blank=True, max_length=50, null=True)),
                ('audit_correction_reference', models.CharField(blank=True, max_length=50, null=True)),
                ('goods_receipt_reference_date', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'db_table': 'sscc_audit_correction_actions',
            },
        ),
        migrations.CreateModel(
            name='SsccAuditCorrectionProductItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mitre_10_item_code', models.CharField(blank=True, max_length=15, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sscc_audit_correction_action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.SsccAuditCorrectionActions')),
            ],
            options={
                'db_table': 'sscc_audit_correction_product_items',
            },
        ),
        migrations.CreateModel(
            name='SsccAuditCorrectionReversal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_by', models.CharField(blank=True, max_length=50, null=True)),
                ('submitted_date_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sscc_audit_correction_reversal',
            },
        ),
        migrations.CreateModel(
            name='SsccAuditCorrections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'sscc_audit_corrections',
            },
        ),
        migrations.CreateModel(
            name='SsccAuditProductItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_barcode', models.CharField(blank=True, max_length=20, null=True)),
                ('mitre10_item_code', models.CharField(blank=True, max_length=15, null=True)),
                ('supplier_item_code', models.CharField(blank=True, max_length=15, null=True)),
                ('item_description', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'sscc_audit_product_items',
            },
        ),
        migrations.CreateModel(
            name='SsccAudits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mandatory_audit_flag', models.IntegerField()),
                ('sscc_labelled_correctly_flag', models.IntegerField()),
                ('sscc_presented_correctly_flag', models.IntegerField()),
                ('audit_comments', models.CharField(blank=True, max_length=2000, null=True)),
                ('audited_by', models.CharField(blank=True, max_length=50, null=True)),
                ('audit_started_date_time', models.DateTimeField(blank=True, null=True)),
                ('audit_completed_date_time', models.DateTimeField(blank=True, null=True)),
                ('sscc', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.Sscc')),
            ],
            options={
                'db_table': 'sscc_audits',
            },
        ),
        migrations.CreateModel(
            name='SsccDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_scanned_date_time', models.DateTimeField(blank=True, null=True)),
                ('sscc_audit_mandated_flag', models.IntegerField(blank=True, null=True)),
                ('first_scanned_by', models.CharField(blank=True, max_length=50, null=True)),
                ('sscc', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.Sscc')),
            ],
            options={
                'db_table': 'sscc_delivery',
            },
        ),
        migrations.CreateModel(
            name='SsccGoodsReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_receipt_reference', models.CharField(blank=True, max_length=50, null=True)),
                ('goods_receipting_process_name', models.CharField(blank=True, max_length=5, null=True)),
                ('goods_receipted_date_time', models.DateTimeField(blank=True, null=True)),
                ('goods_receipted_by', models.CharField(blank=True, max_length=50, null=True)),
                ('goods_receipt_reference_date', models.CharField(blank=True, max_length=15, null=True)),
                ('sscc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.Sscc')),
            ],
            options={
                'db_table': 'sscc_goods_receipt',
            },
        ),
        migrations.CreateModel(
            name='SsccMandatoryAuditControl',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('mitre_10_supplier_code', models.CharField(blank=True, max_length=15, null=True)),
                ('mitre_10_store_code', models.CharField(blank=True, max_length=10, null=True)),
                ('audit_every_nth_sscc', models.IntegerField(blank=True, null=True)),
                ('count_since_last_audit', models.IntegerField(blank=True, null=True)),
                ('supplier_certification_status', models.CharField(blank=True, max_length=50, null=True)),
                ('recount_dollar_threshold', models.FloatField(blank=True, null=True)),
                ('recount_dollar_percent_threshold', models.FloatField(blank=True, null=True)),
                ('expected_deliveries_in_quiet_month', models.IntegerField(blank=True, null=True)),
                ('previous_guaranteed_monthly_audit_date_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sscc_mandatory_audit_control',
            },
        ),
        migrations.CreateModel(
            name='SsccProductItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_barcode', models.CharField(blank=True, max_length=15, null=True)),
                ('mitre_10_item_code', models.CharField(blank=True, max_length=15, null=True)),
                ('supplier_item_code', models.CharField(blank=True, max_length=15, null=True)),
                ('item_description', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sscc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.Sscc')),
            ],
            options={
                'db_table': 'sscc_product_items',
            },
        ),
        migrations.CreateModel(
            name='Synchronisations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_identifier', models.CharField(blank=True, max_length=100, null=True)),
                ('start_event_date_time', models.DateTimeField(blank=True, null=True, unique=True)),
                ('start_control_id', models.IntegerField(blank=True, null=True)),
                ('synchronisation_type', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'synchronisations',
            },
        ),
        migrations.CreateModel(
            name='UnrecognisedSscc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sscc_barcode', models.CharField(blank=True, max_length=20, null=True)),
                ('scanned_date_time', models.DateTimeField(blank=True, null=True)),
                ('scanned_by', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'unrecognised_sscc',
            },
        ),
        migrations.CreateModel(
            name='SynchronisationsEnd',
            fields=[
                ('sync', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='supply_chain.Synchronisations')),
                ('finish_event_date_time', models.DateTimeField(blank=True, null=True, unique=True)),
                ('finishing_control_id', models.IntegerField(blank=True, null=True)),
                ('synchronisation_type', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'synchronisations_end',
            },
        ),
        migrations.AlterUniqueTogether(
            name='ssccmandatoryauditcontrol',
            unique_together=set([('mitre_10_supplier_code', 'mitre_10_store_code')]),
        ),
        migrations.AddField(
            model_name='ssccauditproductitems',
            name='sscc_audit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.SsccAudits'),
        ),
        migrations.AddField(
            model_name='ssccauditcorrections',
            name='sscc_audits',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.SsccAudits'),
        ),
        migrations.AddField(
            model_name='ssccauditcorrectionreversal',
            name='sscc_audit_correction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.SsccAuditCorrections'),
        ),
        migrations.AddField(
            model_name='ssccauditcorrectionactions',
            name='sscc_audit_correction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.SsccAuditCorrections'),
        ),
        migrations.AlterUniqueTogether(
            name='purchaseorders',
            unique_together=set([('purchase_order_reference', 'mitre_10_supplier_code', 'mitre_10_delivery_store_code', 'despatched_date_time')]),
        ),
        migrations.AddField(
            model_name='purchaseorderlineitems',
            name='purchase_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.PurchaseOrders'),
        ),
        migrations.AlterUniqueTogether(
            name='purchaseorderacknowledgements',
            unique_together=set([('message_date_time', 'purchase_order_reference', 'mitre_10_supplier_code', 'mitre_10_delivery_store_code')]),
        ),
        migrations.AddField(
            model_name='purchaseorderacknowledgementlineitems',
            name='purchase_order_acknowledgement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='supply_chain.PurchaseOrderAcknowledgements'),
        ),
        migrations.AlterUniqueTogether(
            name='poexpecteddeliverydate',
            unique_together=set([('purchase_order_reference', 'mitre_10_delivery_store_code', 'mitre_10_supplier_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='asns',
            unique_together=set([('asn_reference', 'mitre_10_supplier_code')]),
        ),
    ]