from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.conf import settings

class ProductConfig(AppConfig):
    name = 'retail.product'

    def ready(self):
        import cbe.signals
        from retail.product.models import Product
        from retail.product.serializers import ProductSerializer

        exchange_prefix = settings.MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name
        exchange_header_list = ('status',)
        
        post_save.connect(  cbe.signals.notify_extra_args(   serializer=ProductSerializer, 
                                                                exchange_prefix=exchange_prefix + ".Product",
                                                                exchange_header_list=exchange_header_list)(cbe.signals.notify_save_instance), 
                            sender=Product, weak=False)    