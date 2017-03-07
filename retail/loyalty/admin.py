from django.contrib import admin

from retail.loyalty.models import LoyaltyTransaction, LoyaltyScheme


class LoyaltySchemeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ('scheme', 'sale', 'promotion','loyalty_amount')
    list_filter = ('scheme', 'sale__datetime', 'sale__store')
    
admin.site.register(LoyaltyScheme, LoyaltySchemeAdmin)    
admin.site.register(LoyaltyTransaction, LoyaltyTransactionAdmin)    