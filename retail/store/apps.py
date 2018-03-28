from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.conf import settings

class StoreConfig(AppConfig):
    name = 'retail.store'

    def ready(self):
        import drf_nest.signals
        from retail.store.models import Store
        from retail.store.serializers import StoreSerializer

        exchange_prefix = settings.MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name
        exchange_header_list = ('store_type', 'store_class',)
        
        post_save.connect(  drf_nest.signals.notify_extra_args(   serializer=StoreSerializer, 
                                                                exchange_prefix=exchange_prefix + ".Store", 
                                                                exchange_header_list=exchange_header_list)(drf_nest.signals.notify_save_instance), 
                            sender=Store, weak=False)