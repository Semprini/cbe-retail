from django.contrib import admin

from retail.product.models import ProductOffering, ProductCategory, Promotion

admin.site.register(ProductOffering)
admin.site.register(ProductCategory)
admin.site.register(Promotion)
