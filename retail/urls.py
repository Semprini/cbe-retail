"""retail URL Configuration
"""

from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.schemas import get_schema_view

from drf_nest.routers import AppRouter
from cbe.urls import apps as cbeapps
from cbe.urls import appurlpatterns as cbeappurlpatterns
import cbe.views as CBEViews

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

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='CBE Retail API')

admin.site.site_title = 'CBE Retail'
admin.site.site_header = 'Retail Business Entities'

storerouter = AppRouter(root_view_name='app-store')
storerouter.register(r'store', StoreViews.StoreViewSet)

productrouter = AppRouter(root_view_name='app-product')
productrouter.register(r'product', ProductViews.ProductViewSet)
productrouter.register(r'product_offering', ProductViews.ProductOfferingViewSet)
productrouter.register(r'supplier_product', ProductViews.SupplierProductViewSet)
productrouter.register(r'product_specification', ProductViews.ProductSpecificationViewSet)
productrouter.register(r'product_category', ProductViews.ProductCategoryViewSet)
productrouter.register(r'product_stock', ProductViews.ProductStockViewSet)
productrouter.register(r'product_stock_take', ProductViews.ProductStockTakeViewSet)
productrouter.register(r'product_association', ProductViews.ProductAssociationViewSet)


pricerouter = AppRouter(root_view_name='app-price')
pricerouter.register(r'price_channel', PriceViews.PriceChannelViewSet)
pricerouter.register(r'price_calculation', PriceViews.PriceCalculationViewSet)
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

customerbillrouter = AppRouter(root_view_name='app-customer_bill')
customerbillrouter.register(r'customer_billing_cycle', CustomerBillViews.CustomerBillingCycleViewSet)
customerbillrouter.register(r'customer_bill_specification', CustomerBillViews.CustomerBillSpecificationViewSet)
customerbillrouter.register(r'customer_bill', CustomerBillViews.CustomerBillViewSet)
customerbillrouter.register(r'account_bill_item', CustomerBillViews.AccountBillItemViewSet)
customerbillrouter.register(r'job_bill_item', CustomerBillViews.JobBillItemViewSet)
customerbillrouter.register(r'subscription_bill_item', CustomerBillViews.SubscriptionBillItemViewSet)
customerbillrouter.register(r'service_bill_item', CustomerBillViews.ServiceBillItemViewSet)
customerbillrouter.register(r'rebate_bill_item', CustomerBillViews.RebateBillItemViewSet)
customerbillrouter.register(r'allocation_bill_item', CustomerBillViews.AllocationBillItemViewSet)
customerbillrouter.register(r'adjustment_bill_item', CustomerBillViews.AdjustmentBillItemViewSet)
customerbillrouter.register(r'dispute_bill_item', CustomerBillViews.DisputeBillItemViewSet)
customerbillrouter.register(r'service_charge', CustomerBillViews.ServiceChargeViewSet)

orderrouter = AppRouter(root_view_name='app-order')
orderrouter.register(r'order', OrderViews.OrderViewSet)
orderrouter.register(r'quote', OrderViews.QuoteViewSet)
orderrouter.register(r'order_item', OrderViews.OrderItemViewSet)

supplychainrouter = AppRouter(root_view_name='app-supply_chain')
supplychainrouter.register(r'asns', SupplyChainViews.AsnsViewSet)
supplychainrouter.register(r'po_expected_delivery_date', SupplyChainViews.PoExpectedDeliveryDateViewSet)
supplychainrouter.register(r'purchase_order_acknowledgement_line_items', SupplyChainViews.PurchaseOrderAcknowledgementLineItemsViewSet)
supplychainrouter.register(r'purchase_order_acknowledgements', SupplyChainViews.PurchaseOrderAcknowledgementsViewSet)
supplychainrouter.register(r'purchase_order_line_items', SupplyChainViews.PurchaseOrderLineItemsViewSet)
supplychainrouter.register(r'purchase_order', SupplyChainViews.PurchaseOrderViewSet)
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
                            'price':'app-price',
                            'promotion':'app-promotion',
                            'sale':'app-sale',
                            'loyalty':'app-loyalty',
                            'market':'app-market',
                            'customer_bill':'app-customer_bill',
                            'order':'app-order',
                            'supply_chain':'app-supply_chain',
                            'job_management':'app-job_management', }
router = AppRouter(  apps={**apps,**cbeapps} )
router.register(r'auth/users', CBEViews.UserViewSet)
router.register(r'content_types', CBEViews.ContentTypeViewSet)
        
urlpatterns = [
    url(r'^$', schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^explorer/', include('explorer.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api/store/', include(storerouter.urls)),
    url(r'^api/product/', include(productrouter.urls)),
    url(r'^api/price/', include(pricerouter.urls)),
    url(r'^api/sale/', include(salerouter.urls)),
    url(r'^api/order/', include(orderrouter.urls)),
    url(r'^api/loyalty/', include(loyaltyrouter.urls)),
    url(r'^api/market/', include(marketrouter.urls)),
    url(r'^api/customer_bill/', include(customerbillrouter.urls)),
    url(r'^api/supply_chain/', include(supplychainrouter.urls)),
    url(r'^api/job_management/', include(jobmanagementrouter.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ] + cbeappurlpatterns
