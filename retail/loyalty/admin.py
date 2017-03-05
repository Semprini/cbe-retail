from django.contrib import admin

from retail.loyalty.models import LoyaltyTransaction, LoyaltyCard, LoyaltyScheme, LoyaltyCardType


class LoyaltySchemeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    
class LoyaltyCardTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    
class LoyaltyCardAdmin(admin.ModelAdmin):
    list_display = ('identification_type', 'number', 'party',)
    list_filter = ('identification_type',)
    
    
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ('scheme', 'sale', 'promotion','loyalty_amount')
    list_filter = ('scheme', 'sale__datetime', 'sale__store')
    
admin.site.register(LoyaltyScheme, LoyaltySchemeAdmin)    
admin.site.register(LoyaltyCardType, LoyaltyCardTypeAdmin)    
admin.site.register(LoyaltyCard, LoyaltyCardAdmin)    
admin.site.register(LoyaltyTransaction, LoyaltyTransactionAdmin)    