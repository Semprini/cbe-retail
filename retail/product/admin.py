from django.contrib import admin

from retail.product.models import Product, ProductOffering, ProductCategory, ProductStock, ProductStockTake

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ( 'code', 'level', 'name', 'description', )
    list_filter = ( 'level', )

class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'code', 'status', 'name', 'brand', 'sub_brand', 'tax_code', 'impulse_item', 'key_value_item', 'core_abc', 'core_range', 'range', 'dangerous_classification', 'relative_importance_index', 'exclusive' )
    list_filter = ( 'status','impulse_item', 'key_value_item', 'core_abc', 'range' )
    raw_id_fields = ('parent','bundle')
    search_fields = ['code','name']

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOffering)
admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(ProductStock)
admin.site.register(ProductStockTake)

