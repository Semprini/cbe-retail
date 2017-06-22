from django.contrib import admin

from retail.customer_bill.models import CustomerBillingCycle, CustomerBillSpecification, CustomerBill, AccountBillItem, SubscriptionBillItem, ServiceBillItem, RebateBillItem, AllocationBillItem, AdjustmentBillItem, DisputeBillItem

admin.site.register( CustomerBillingCycle)
admin.site.register( CustomerBillSpecification )
admin.site.register( CustomerBill )
admin.site.register( AccountBillItem )
admin.site.register( SubscriptionBillItem )
admin.site.register( ServiceBillItem )
admin.site.register( RebateBillItem )
admin.site.register( AllocationBillItem )
admin.site.register( AdjustmentBillItem )
admin.site.register( DisputeBillItem )

