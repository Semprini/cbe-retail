from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from retail.settings import MQ_FRAMEWORK

class SaleConfig(AppConfig):
    name = 'retail.sale'

    def ready(self):
        import retail.signals
        from retail.sale.models import Sale
        from retail.sale.serializers import SaleSerializer

        exchange_prefix = MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name
        exchange_header_list = ('store',)
        
        post_save.connect(  retail.signals.notify_extra_args(   serializer=SaleSerializer, 
                                                                exchange_prefix=exchange_prefix, 
                                                                exchange_header_list=exchange_header_list)(retail.signals.notify_save_instance), 
                            sender=Sale, weak=False)
