from django.contrib import admin

from retail.customer_bill.models import CustomerBillingCycle, CustomerBillSpecification, CustomerBill, AccountBillItem, JobBillItem, SubscriptionBillItem, ServiceBillItem, RebateBillItem, AllocationBillItem, AdjustmentBillItem, DisputeBillItem

class AccountBillItemInline(admin.TabularInline):
    model = AccountBillItem
    extra = 0

class JobBillItemInline(admin.TabularInline):
    model = JobBillItem
    extra = 0

class CustomerBillAdmin(admin.ModelAdmin):
    list_display = ('account', 'specification', 'number','period_from','period_to','status')
    list_filter = ('period_from', 'status',)
    inlines = [ AccountBillItemInline, JobBillItemInline, ]
    
admin.site.register( CustomerBillingCycle)
admin.site.register( CustomerBillSpecification )
admin.site.register( CustomerBill,CustomerBillAdmin )
admin.site.register( AccountBillItem )
admin.site.register( JobBillItem )
admin.site.register( SubscriptionBillItem )
admin.site.register( ServiceBillItem )
admin.site.register( RebateBillItem )
admin.site.register( AllocationBillItem )
admin.site.register( AdjustmentBillItem )
admin.site.register( DisputeBillItem )

