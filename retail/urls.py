"""retail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework import serializers, viewsets

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from cbe.urls import cberouter

import retail.store.views as StoreViews
import retail.product.views as ProductViews
import retail.sale.views as SaleViews
import retail.loyalty.views as LoyaltyViews
import retail.market.views as MarketViews
import retail.pricing.views as PriceViews
import retail.customer_bill.views as CustomerBillViews
import retail.order.views as OrderViews
import retail.supply_chain.views as SupplyChainViews
import retail.job_management.views as JobManagmentViews

admin.site.site_title = 'CBE Retail'
admin.site.site_header = 'Retail Business Entities'

retailrouter = DefaultRouter()
retailrouter.register(r'store/store', StoreViews.StoreViewSet)

retailrouter.register(r'product/product', ProductViews.ProductViewSet)
retailrouter.register(r'product/product_offering', ProductViews.ProductOfferingViewSet)
retailrouter.register(r'product/product_category', ProductViews.ProductCategoryViewSet)
retailrouter.register(r'product/product_stock_level', ProductViews.ProductStockLevelViewSet)

retailrouter.register(r'price/promotion', PriceViews.PromotionViewSet)
retailrouter.register(r'price/product_offering_price', PriceViews.ProductOfferingPriceViewSet)

retailrouter.register(r'sale/sales_channel', SaleViews.SalesChannelViewSet)
retailrouter.register(r'sale/sale', SaleViews.SaleViewSet)
retailrouter.register(r'sale/sale_item', SaleViews.SaleItemViewSet)
retailrouter.register(r'sale/tender', SaleViews.TenderViewSet)
retailrouter.register(r'sale/tender_type', SaleViews.TenderTypeViewSet)
retailrouter.register(r'sale/purchaser', SaleViews.PurchaserViewSet)

retailrouter.register(r'loyalty/loyalty_transaction', LoyaltyViews.LoyaltyTransactionViewSet)
retailrouter.register(r'loyalty/loyalty_scheme', LoyaltyViews.LoyaltySchemeViewSet)

retailrouter.register(r'market/market_segment', MarketViews.MarketSegmentViewSet)
retailrouter.register(r'market/market_strategy', MarketViews.MarketStrategyViewSet)

retailrouter.register(r'customer_bill/customer_billing_cycle', CustomerBillViews.CustomerBillingCycleViewSet)
retailrouter.register(r'customer_bill/customer_bill_specification', CustomerBillViews.CustomerBillSpecificationViewSet)
retailrouter.register(r'customer_bill/customer_bill', CustomerBillViews.CustomerBillViewSet)

retailrouter.register(r'customer_bill/account_bill_item', CustomerBillViews.AccountBillItemViewSet)
retailrouter.register(r'customer_bill/subscription_bill_item', CustomerBillViews.SubscriptionBillItemViewSet)
retailrouter.register(r'customer_bill/service_bill_item', CustomerBillViews.ServiceBillItemViewSet)
retailrouter.register(r'customer_bill/rebate_bill_item', CustomerBillViews.RebateBillItemViewSet)
retailrouter.register(r'customer_bill/allocation_bill_item', CustomerBillViews.AllocationBillItemViewSet)
retailrouter.register(r'customer_bill/adjustment_bill_item', CustomerBillViews.AdjustmentBillItemViewSet)
retailrouter.register(r'customer_bill/dispute_bill_item', CustomerBillViews.DisputeBillItemViewSet)

retailrouter.register(r'order/order', OrderViews.OrderViewSet)
retailrouter.register(r'order/order_item', OrderViews.OrderItemViewSet)

retailrouter.register(r'supply_chain/asns', SupplyChainViews.AsnsViewSet)
retailrouter.register(r'supply_chain/po_expected_delivery_date', SupplyChainViews.PoExpectedDeliveryDateViewSet)
retailrouter.register(r'supply_chain/purchase_order_acknowledgement_line_items', SupplyChainViews.PurchaseOrderAcknowledgementLineItemsViewSet)
retailrouter.register(r'supply_chain/purchase_order_acknowledgements', SupplyChainViews.PurchaseOrderAcknowledgementsViewSet)
retailrouter.register(r'supply_chain/purchase_order_line_items', SupplyChainViews.PurchaseOrderLineItemsViewSet)
retailrouter.register(r'supply_chain/purchase_order', SupplyChainViews.PurchaseOrdersViewSet)
retailrouter.register(r'supply_chain/schema_version', SupplyChainViews.SchemaVersionViewSet)
retailrouter.register(r'supply_chain/sscc', SupplyChainViews.SsccViewSet)
retailrouter.register(r'supply_chain/sscc_audit_correction_actions', SupplyChainViews.SsccAuditCorrectionActionsViewSet)
retailrouter.register(r'supply_chain/sscc_audit_correction_product_items', SupplyChainViews.SsccAuditCorrectionProductItemsViewSet)
retailrouter.register(r'supply_chain/sscc_audit_correction_reversal', SupplyChainViews.SsccAuditCorrectionReversalViewSet)
retailrouter.register(r'supply_chain/sscc_audit_corrections', SupplyChainViews.SsccAuditCorrectionsViewSet)
retailrouter.register(r'supply_chain/sscc_audit_product_items', SupplyChainViews.SsccAuditProductItemsViewSet)
retailrouter.register(r'supply_chain/sscc_audits', SupplyChainViews.SsccAuditsViewSet)
retailrouter.register(r'supply_chain/sscc_delivery', SupplyChainViews.SsccDeliveryViewSet)
retailrouter.register(r'supply_chain/sscc_goods_receipt', SupplyChainViews.SsccGoodsReceiptViewSet)
retailrouter.register(r'supply_chain/sscc_mandatory_audit_control', SupplyChainViews.SsccMandatoryAuditControlViewSet)
retailrouter.register(r'supply_chain/sscc_product_items', SupplyChainViews.SsccProductItemsViewSet)
retailrouter.register(r'supply_chain/synchronisations', SupplyChainViews.SynchronisationsViewSet)
retailrouter.register(r'supply_chain/synchronisations_end', SupplyChainViews.SynchronisationsEndViewSet)
retailrouter.register(r'supply_chain/unrecognised_sscc', SupplyChainViews.UnrecognisedSsccViewSet)

retailrouter.register(r'job_management/job', JobManagmentViews.JobViewSet)
retailrouter.register(r'job_management/job_party_role', JobManagmentViews.JobPartyRoleViewSet)

router = DefaultRouter()
for route in retailrouter.registry:
    router.register(route[0], route[1])
for route in cberouter.registry:
    if len(route) == 2:
        router.register(route[0], route[1])
    else:
        router.register(route[0], route[1], base_name=route[2])
        
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    ]
