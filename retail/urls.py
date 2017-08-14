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

from django.views.generic import View
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from rest_framework import routers
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework import serializers, viewsets
from rest_framework import generics
from django.urls import reverse

from cbe.routers import AppRouter
from cbe.urls import apps as cbeapps
from cbe.urls import appurlpatterns as cbeappurlpatterns

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

storerouter = AppRouter(root_view_name='app-store')
storerouter.register(r'store', StoreViews.StoreViewSet)

productrouter = AppRouter(root_view_name='app-product')
productrouter.register(r'product', ProductViews.ProductViewSet)
productrouter.register(r'product_offering', ProductViews.ProductOfferingViewSet)
productrouter.register(r'product_category', ProductViews.ProductCategoryViewSet)
productrouter.register(r'product_stock_level', ProductViews.ProductStockLevelViewSet)

pricerouter = AppRouter(root_view_name='app-promotion')
pricerouter.register(r'promotion', PriceViews.PromotionViewSet)
pricerouter.register(r'product_offering_price', PriceViews.ProductOfferingPriceViewSet)

salerouter = AppRouter(root_view_name='app-sale')
salerouter.register(r'sales_channel', SaleViews.SalesChannelViewSet)
salerouter.register(r'sale', SaleViews.SaleViewSet)
salerouter.register(r'sale_item', SaleViews.SaleItemViewSet)
salerouter.register(r'tender', SaleViews.TenderViewSet)
salerouter.register(r'tender_type', SaleViews.TenderTypeViewSet)
salerouter.register(r'purchaser', SaleViews.PurchaserViewSet)

loyaltyrouter = AppRouter(root_view_name='app-loyalty')
loyaltyrouter.register(r'loyalty_transaction', LoyaltyViews.LoyaltyTransactionViewSet)
loyaltyrouter.register(r'loyalty_scheme', LoyaltyViews.LoyaltySchemeViewSet)

marketrouter = AppRouter(root_view_name='app-market')
marketrouter.register(r'market_segment', MarketViews.MarketSegmentViewSet)
marketrouter.register(r'market_strategy', MarketViews.MarketStrategyViewSet)

customerbillrouter = AppRouter(root_view_name='app-customer_billing')
customerbillrouter.register(r'customer_billing_cycle', CustomerBillViews.CustomerBillingCycleViewSet)
customerbillrouter.register(r'customer_bill_specification', CustomerBillViews.CustomerBillSpecificationViewSet)
customerbillrouter.register(r'customer_bill', CustomerBillViews.CustomerBillViewSet)
customerbillrouter.register(r'account_bill_item', CustomerBillViews.AccountBillItemViewSet)
customerbillrouter.register(r'subscription_bill_item', CustomerBillViews.SubscriptionBillItemViewSet)
customerbillrouter.register(r'service_bill_item', CustomerBillViews.ServiceBillItemViewSet)
customerbillrouter.register(r'rebate_bill_item', CustomerBillViews.RebateBillItemViewSet)
customerbillrouter.register(r'allocation_bill_item', CustomerBillViews.AllocationBillItemViewSet)
customerbillrouter.register(r'adjustment_bill_item', CustomerBillViews.AdjustmentBillItemViewSet)
customerbillrouter.register(r'dispute_bill_item', CustomerBillViews.DisputeBillItemViewSet)

orderrouter = AppRouter(root_view_name='app-order')
orderrouter.register(r'order', OrderViews.OrderViewSet)
orderrouter.register(r'order_item', OrderViews.OrderItemViewSet)

supplychainrouter = AppRouter(root_view_name='app-supply_chain')
supplychainrouter.register(r'asns', SupplyChainViews.AsnsViewSet)
supplychainrouter.register(r'po_expected_delivery_date', SupplyChainViews.PoExpectedDeliveryDateViewSet)
supplychainrouter.register(r'purchase_order_acknowledgement_line_items', SupplyChainViews.PurchaseOrderAcknowledgementLineItemsViewSet)
supplychainrouter.register(r'purchase_order_acknowledgements', SupplyChainViews.PurchaseOrderAcknowledgementsViewSet)
supplychainrouter.register(r'purchase_order_line_items', SupplyChainViews.PurchaseOrderLineItemsViewSet)
supplychainrouter.register(r'purchase_order', SupplyChainViews.PurchaseOrdersViewSet)
supplychainrouter.register(r'schema_version', SupplyChainViews.SchemaVersionViewSet)
supplychainrouter.register(r'sscc', SupplyChainViews.SsccViewSet)
supplychainrouter.register(r'sscc_audit_correction_actions', SupplyChainViews.SsccAuditCorrectionActionsViewSet)
supplychainrouter.register(r'sscc_audit_correction_product_items', SupplyChainViews.SsccAuditCorrectionProductItemsViewSet)
supplychainrouter.register(r'sscc_audit_correction_reversal', SupplyChainViews.SsccAuditCorrectionReversalViewSet)
supplychainrouter.register(r'sscc_audit_corrections', SupplyChainViews.SsccAuditCorrectionsViewSet)
supplychainrouter.register(r'sscc_audit_product_items', SupplyChainViews.SsccAuditProductItemsViewSet)
supplychainrouter.register(r'sscc_audits', SupplyChainViews.SsccAuditsViewSet)
supplychainrouter.register(r'sscc_delivery', SupplyChainViews.SsccDeliveryViewSet)
supplychainrouter.register(r'sscc_goods_receipt', SupplyChainViews.SsccGoodsReceiptViewSet)
supplychainrouter.register(r'sscc_mandatory_audit_control', SupplyChainViews.SsccMandatoryAuditControlViewSet)
supplychainrouter.register(r'sscc_product_items', SupplyChainViews.SsccProductItemsViewSet)
supplychainrouter.register(r'synchronisations', SupplyChainViews.SynchronisationsViewSet)
supplychainrouter.register(r'synchronisations_end', SupplyChainViews.SynchronisationsEndViewSet)
supplychainrouter.register(r'unrecognised_sscc', SupplyChainViews.UnrecognisedSsccViewSet)

jobmanagementrouter = AppRouter(root_view_name='app-job_management')
jobmanagementrouter.register(r'job', JobManagmentViews.JobViewSet)
jobmanagementrouter.register(r'job_party_role', JobManagmentViews.JobPartyRoleViewSet)

apps={                      'store':'app-store',
                            'product':'app-product',
                            'promotion':'app-promotion',
                            'sale':'app-sale',
                            'loyalty':'app-loyalty',
                            'market':'app-market',
                            'customer_billing':'app-customer_billing',
                            'order':'app-order',
                            'supply_chain':'app-supply_chain',
                            'job_management':'app-job_management', }
router = AppRouter(  apps={**apps,**cbeapps} )
        
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api/store/', include(storerouter.urls)),
    url(r'^api/product/', include(productrouter.urls)),
    url(r'^api/price/', include(pricerouter.urls)),
    url(r'^api/sale/', include(salerouter.urls)),
    url(r'^api/loyalty/', include(loyaltyrouter.urls)),
    url(r'^api/market/', include(marketrouter.urls)),
    url(r'^api/customer_bill/', include(customerbillrouter.urls)),
    url(r'^api/supply_chain/', include(supplychainrouter.urls)),
    url(r'^api/job_management/', include(jobmanagementrouter.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ] + cbeappurlpatterns
