from django.contrib import admin

from retail.pricing.models import PriceChannel, PriceCalculation, Promotion, ProductOfferingPrice


admin.site.register(PriceChannel)    
admin.site.register(PriceCalculation)
admin.site.register(Promotion)    
admin.site.register(ProductOfferingPrice)
