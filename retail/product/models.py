from django.db import models
from django.db.models import Q

from cbe.party.models import Organisation
from cbe.location.models import Location
from cbe.supplier_partner.models import Supplier, Buyer
from cbe.human_resources.models import Staff

from retail.store.models import Store
from retail.market.models import MarketSegment, MarketStrategy


class ProductCategory(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    parent = models.ForeignKey('ProductCategory', null=True,blank=True)

    level = models.CharField(max_length=200, choices=(('department', 'department'), ('subdepartment', 'subdepartment'), ('fineline', 'fineline'), ))
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

        
class ProductAssociation(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    
    from_product = models.ForeignKey('Product', related_name='from_products')
    to_product = models.ForeignKey('Product', related_name='to_products')

    association_type = models.CharField(max_length=200, choices=(('cross-selling', 'cross-selling'), ('other', 'other'), ), default='cross-selling')
    rank = models.IntegerField( default=0 )
    
       
class Product(models.Model):
    code = models.CharField(max_length=50, null=True, blank=True)

    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200, choices=(('active', 'active'), ('inactive', 'inactive'), ), default='active')

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    bundle = models.ManyToManyField('Product', blank=True)
    categories = models.ManyToManyField(ProductCategory, blank=True)

    associated_products = models.ManyToManyField('self', through='ProductAssociation',
                                           symmetrical=False,
                                           related_name='associated_to+')

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.name

    def add_association(self, product, type, rank, symm=True):
        association, created = ProductAssociation.objects.get_or_create(
            from_product=self,
            to_product=product,
            association_type=type,
            rank=rank)
        if symm:
            # avoid recursion by passing `symm=False`
            product.add_association(self, type, rank, False)
        return association

    def remove_association(self, product, type, rank, symm=True):
        ProductAssociation.objects.filter(
            from_person=self,
            to_product=product,
            association_type=type,
            rank=rank).delete()
        if symm:
            # avoid recursion by passing `symm=False`
            product.remove_association(self, type, rank, False)

    @property
    def cross_sell_products(self):
        return Product.objects.filter( 
            (Q(to_products__association_type='cross-selling') | Q(from_products__association_type='cross-selling') ) &
            (Q(to_products__from_product=self) | Q(from_products__to_product=self) )
            ).order_by('to_products__rank','from_products__rank',)
            
    @property
    def product_associations(self):
        return ProductAssociation.objects.filter(
            Q(from_product=self) | Q(to_product=self)            )

            
    def get_associations_by_type(self, type):
        return self.associated_products.filter(
            to_products__association_type=type,
            to_products__from_product=self)            

            
class SupplierProduct(models.Model):
    supplier_sku = models.CharField(max_length=200, primary_key=True)
    barcode = models.CharField(max_length=50, null=True, blank=True)

    product = models.ForeignKey(Product)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)

    buyer = models.ForeignKey(Buyer, null=True, blank=True)

    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('meter', 'meter')), default='each')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    reccomended_retail_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['supplier_sku']
    
    def __str__(self):
        return "%s" %(self.product.name)
    
    
class ProductOffering(models.Model):
    sku = models.CharField(max_length=50, primary_key=True)
    product = models.ForeignKey(Product, related_name="product_offerings")
    barcode = models.CharField(max_length=50, null=True, blank=True)

    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200, choices=(('active', 'active'), ('inactive', 'inactive'), ), default='active')

    channels = models.ManyToManyField('sale.SalesChannel', blank=True)
    segments = models.ManyToManyField(MarketSegment, blank=True)
    strategies = models.ManyToManyField(MarketStrategy, blank=True)
    
    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('meter', 'meter')), default='each')
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    average_cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['sku']
    
    def __str__(self):
        return "%s" %(self.product.name)

        
class ProductStock(models.Model):
    product = models.ForeignKey(Product, related_name='product_stock')
    store = models.ForeignKey(Store)
    location = models.ForeignKey(Location, null=True, blank=True)

    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('meter', 'meter')), default='each')
    amount = models.DecimalField(max_digits=8, decimal_places=4)
    average = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    reorder_minimum = models.DecimalField(max_digits=8, decimal_places=4)

    def __str__(self):
        return "%s:%d"%(self.product.name, self.amount)

        
class ProductStockTake(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    product_stock = models.ForeignKey(ProductStock, related_name='product_stock_takes')

    store = models.ForeignKey(Store)
    location = models.ForeignKey(Location, null=True, blank=True)
    staff = models.ForeignKey(Staff, null=True, blank=True)

    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('meter', 'meter')), default='each')
    amount = models.DecimalField(max_digits=8, decimal_places=4)
    