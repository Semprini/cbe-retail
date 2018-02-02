from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.admin import GenericTabularInline

from cbe.party.admin import GenericPartyRoleAdminForm, GenericPartyRoleAdmin
from cbe.human_resources.models import Identification
from retail.store.models import Store


class StoreAdminForm(GenericPartyRoleAdminForm):

    class Meta:
        exclude = []#['contact_mediums',]
        model = Store

class IdentifiersInline(GenericTabularInline):
    model = Identification
    ct_field = 'party_role_content_type'
    ct_fk_field = 'party_role_object_id'
    extra = 1
        
class StoreAdmin(GenericPartyRoleAdmin):
    list_display = ('enterprise_id', 'code', 'store_type','store_class','party',)
    form = StoreAdminForm
    fields = (
        'name', 'enterprise_id', 'code', 'store_type','store_class','party','opening_date', 'location', 'trade_area', 'retail_area', 'national_area', 'buildings')
    #readonly_fields = ('name',)
    inlines = [IdentifiersInline, ]
    
admin.site.register(Store, StoreAdmin)
