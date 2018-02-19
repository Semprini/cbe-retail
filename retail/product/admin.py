from django.contrib import admin

from retail.product.models import Product, ProductOffering, ProductCategory, ProductStock, ProductStockTake

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ( 'code', 'level', 'name', 'description', )
    list_filter = ( 'level', )


admin.site.register(Product)
admin.site.register(ProductOffering)
admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(ProductStock)
admin.site.register(ProductStockTake)

