from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.conf import settings

class SaleConfig(AppConfig):
    name = 'retail.sale'

    def ready(self):
        import drf_nest.signals
        from retail.sale.models import Sale
        from retail.sale.serializers import SaleSerializer

        exchange_prefix = settings.MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name
        exchange_header_list = ('store',)
        
        post_save.connect(  drf_nest.signals.notify_extra_args(   serializer=SaleSerializer, 
                                                                exchange_prefix=exchange_prefix + ".Sale", 
                                                                exchange_header_list=exchange_header_list)(drf_nest.signals.notify_save_instance), 
                            sender=Sale, weak=False)
