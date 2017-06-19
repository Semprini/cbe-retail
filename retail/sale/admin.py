from django.contrib import admin

from retail.sale.models import Sale, SaleItem, TenderType, Tender, RetailChannel
from retail.loyalty.models import LoyaltyTransaction

class TenderInline(admin.TabularInline):
    model = Tender
    extra = 0

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0

class LoyaltyTransactionInline(admin.TabularInline):
    model = LoyaltyTransaction
    extra = 0
    

class SaleAdmin(admin.ModelAdmin):
    list_display = ('location', 'seller', 'datetime','staff','docket_number','total_amount','total_discount')
    list_filter = ('datetime', 'seller')
    inlines = [ TenderInline, SaleItemInline, LoyaltyTransactionInline]


   
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem)
admin.site.register(TenderType)
admin.site.register(Tender)
admin.site.register(RetailChannel)
