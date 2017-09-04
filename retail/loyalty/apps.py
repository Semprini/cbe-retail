from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from django.conf import settings

class LoyaltyConfig(AppConfig):
    name = 'retail.loyalty'

    def ready(self):
        import cbe.signals
        from retail.loyalty.models import LoyaltyTransaction
        from retail.loyalty.serializers import LoyaltyTransactionSerializer

        exchange_prefix = settings.MQ_FRAMEWORK['EXCHANGE_PREFIX'] + self.name
        exchange_header_list = ('scheme',)
        
        post_save.connect(  cbe.signals.notify_extra_args(   serializer=LoyaltyTransactionSerializer, 
                                                                exchange_prefix=exchange_prefix + ".LoyaltyTransaction",
                                                                exchange_header_list=exchange_header_list)(cbe.signals.notify_save_instance), 
                            sender=LoyaltyTransaction, weak=False)    