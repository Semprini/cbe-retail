from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.conf import settings

class ProductConfig(AppConfig):
    name = 'retail.product'

    def ready(self):
        import drf_nest.signals
        from retail.product.models import Product, ProductOffering, SupplierProduct
        from retail.product.serializers import ProductSerializer, ProductOfferingSerializer, SupplierProductSerializer

        exchange_prefix = settings.MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name
        
        product_exchange_header_list = ('status',)
        post_save.connect(  drf_nest.signals.notify_extra_args(   serializer=ProductSerializer, 
                                                                exchange_prefix=exchange_prefix + ".Product",
                                                                exchange_header_list=product_exchange_header_list)(drf_nest.signals.notify_save_instance), 
                            sender=Product, weak=False)

        offering_exchange_header_list = ('department', 'sub_department', 'fineline',)
        post_save.connect(  drf_nest.signals.notify_extra_args(   serializer=ProductOfferingSerializer, 
                                                                exchange_prefix=exchange_prefix + ".ProductOffering",
                                                                exchange_header_list=offering_exchange_header_list)(drf_nest.signals.notify_save_instance), 
                            sender=ProductOffering, weak=False)

        sp_exchange_header_list = ()
        post_save.connect(  drf_nest.signals.notify_extra_args(   serializer=SupplierProductSerializer, 
                                                                exchange_prefix=exchange_prefix + ".SupplierProduct",
                                                                exchange_header_list=sp_exchange_header_list)(drf_nest.signals.notify_save_instance), 
                            sender=SupplierProduct, weak=False)
