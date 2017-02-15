from django.contrib import admin

from retail.sale.models import Sale, SaleItem, TenderType, Tender, LoyaltyTransaction

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
    list_display = ('store', 'datetime','docket_number','total_amount')
    list_filter = ('datetime', 'store')
    inlines = [ TenderInline, SaleItemInline, LoyaltyTransactionInline]

class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ('sale', 'promotion','amount')
    #list_filter = ('sale__datetime', 'sale__store')
    


admin.site.register(LoyaltyTransaction, LoyaltyTransactionAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem)
admin.site.register(TenderType)
admin.site.register(Tender)
