from django.contrib import admin

from retail.product.models import Product, ProductOffering, ProductCategory, ProductStock, ProductStockTake

admin.site.register(Product)
admin.site.register(ProductOffering)
admin.site.register(ProductCategory)
admin.site.register(ProductStock)
admin.site.register(ProductStockTake)

