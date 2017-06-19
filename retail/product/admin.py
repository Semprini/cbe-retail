from django.contrib import admin

from retail.product.models import Product, ProductOffering, ProductCategory, ProductStockLevel

admin.site.register(Product)
admin.site.register(ProductOffering)
admin.site.register(ProductCategory)
admin.site.register(ProductStockLevel)

