from django.contrib import admin

from retail.product.models import Product, ProductOffering, ProductCategory, ProductStock, ProductStockTake, SupplierProduct

class DepartmentListFilter(admin.SimpleListFilter):
    title = 'department'
    parameter_name = 'department'
    def lookups(self, request, model_admin):
        result = ProductCategory.objects.filter(level='department')
        return [(str(x.id), x) for x in result]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(department__id=self.value())
        else:
            return queryset

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ( 'code', 'level', 'name', 'description', )
    list_filter = ( 'level', )

class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'code', 'status', 'name', 'brand', 'sub_brand', 'tax_code', 'impulse_item', 'key_value_item', 'core_abc', 'core_range', 'range', 'dangerous_classification', 'relative_importance_index', 'exclusive' )
    list_filter = ( 'status','impulse_item', 'key_value_item', 'core_abc', 'range' )
    raw_id_fields = ('parent','bundle')
    search_fields = ['code','name']

    
class ProductOfferingAdmin(admin.ModelAdmin):
    list_display = ( 'sku', 'product', 'department', 'sub_department', 'fineline', 'unit_of_measure', 'retail_price', 'average_cost_price', )
    list_filter = ( 'unit_of_measure',DepartmentListFilter,  )
    raw_id_fields = ('product',)
    search_fields = ['sku','product']

class SupplierProductAdmin(admin.ModelAdmin):
    list_display = ( 'supplier_sku', 'barcode', 'product', 'supplier', 'buyer', 'unit_of_measure', 'reccomended_retail_price', 'cost_price', )
    list_filter = ( 'unit_of_measure','supplier',  )
    raw_id_fields = ('product',)
    search_fields = ['supplier_sku','product']
    
admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOffering, ProductOfferingAdmin)
admin.site.register(SupplierProduct, SupplierProductAdmin)
admin.site.register(ProductStock)
admin.site.register(ProductStockTake)


