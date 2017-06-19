from django.contrib import admin

from retail.product.models import ProductOffering, ProductOfferingPrice, ProductCategory, Promotion

admin.site.register(ProductOffering)
admin.site.register(ProductOfferingPrice)
admin.site.register(ProductCategory)
admin.site.register(Promotion)
