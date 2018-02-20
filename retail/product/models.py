from django.db import models
from django.db.models import Q

from cbe.party.models import Organisation
from cbe.location.models import Location
from cbe.supplier_partner.models import Supplier, Buyer
from cbe.human_resources.models import Staff

from retail.store.models import Store
from retail.market.models import MarketSegment, MarketStrategy

PRODUCT_EXCLUSIVE_CHOICES=( ('RE','Retail Exclusive'), ('E','Exclusive'), ('P','Proprietary'), ('BTR','Better'), ('BES','Best'), ('BTY','BTY') )

class ProductCategory(models.Model):
    code = models.IntegerField()
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    parent = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, null=True,blank=True)

    level = models.CharField(max_length=200, choices=(('division', 'division'),('category', 'category'),('department', 'department'), ('sub_department', 'sub_department'), ('fineline', 'fineline'), ))
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

        
class ProductAssociation(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    
    from_product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='from_products')
    to_product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='to_products')

    association_type = models.CharField(max_length=200, choices=(('cross-selling', 'cross-selling'), ('other', 'other'), ), default='cross-selling')
    rank = models.IntegerField( default=0 )

    
class Product(models.Model):
    parent = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, related_name='child_products')
    code = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=100, blank=True)
    sub_brand = models.CharField(max_length=100, blank=True)

    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200, choices=(('active', 'active'), ('inactive', 'inactive'), ), default='active')

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tax_code = models.CharField(max_length=50)
    impulse_item = models.BooleanField(default=False)
    key_value_item = models.BooleanField(default=False)
    first_sale_date = models.DateField(null=True, blank=True)
    core_abc = models.BooleanField(default=False)               # is this just kvi?
    core_range = models.BooleanField(default=False)
    range = models.IntegerField( default=0 )
    dangerous_classification = models.CharField(max_length=50, blank=True)
    relative_importance_index = models.CharField(max_length=10, blank=True)
    exclusive = models.CharField(max_length=50, blank=True, choices=PRODUCT_EXCLUSIVE_CHOICES)

    business_unit = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True, blank=True)
    
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

            
class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    
    colour_name = models.CharField(max_length=50, null=True, blank=True)
    colour_value = models.CharField(max_length=50, null=True, blank=True)
    
    size_name = models.CharField(max_length=50, null=True, blank=True)
    size_value = models.CharField(max_length=50, null=True, blank=True)

            
class SupplierProduct(models.Model):
    supplier_sku = models.CharField(max_length=200)
    barcode = models.CharField(max_length=50, null=True, blank=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="supplier_products")
    specification = models.ForeignKey(ProductSpecification, on_delete=models.CASCADE, related_name="supplier_products", null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)

    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('meter', 'meter')), default='each')
    carton_quantity = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reccomended_retail_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reccomended_markup = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    next_available_date = models.DateField(null=True, blank=True)

    quantity_break1 = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    quantity_price1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity_break2 = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    quantity_price2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['supplier_sku']
    
    def __str__(self):
        return "%s" %(self.product.name)
    
    
class ProductOffering(models.Model):
    sku = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_offerings")
    specification = models.ForeignKey(ProductSpecification, on_delete=models.CASCADE, related_name="product_offerings", null=True, blank=True)
    barcode = models.CharField(max_length=50, null=True, blank=True)

    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200, choices=(('active', 'active'), ('inactive', 'inactive'), ), default='active')
    type = models.CharField(max_length=100, choices=(('standard','standard'), ('fractional','fractional'), ('kit','kit')), default='standard')

    channels = models.ManyToManyField('sale.SalesChannel', blank=True)
    segments = models.ManyToManyField(MarketSegment, blank=True)
    strategies = models.ManyToManyField(MarketStrategy, blank=True)
    
    department = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='department_offerings', null=True, blank=True)
    sub_department = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='sub_department_offerings', null=True, blank=True)
    fineline = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='fineline_offerings', null=True, blank=True)
    
    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('meter', 'meter')), default='each')
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    average_cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['sku']
    
    def __str__(self):
        return "%s" %(self.product.name)

        
class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_stock')
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    updated_date = models.DateField(null=True, blank=True)

    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('meter', 'meter')), default='each')
    amount = models.DecimalField(max_digits=8, decimal_places=4)
    average = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    reorder_minimum = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return "%s:%d"%(self.product.name, self.amount)

        
class ProductStockTake(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    product_stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE, related_name='product_stock_takes')

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)

    unit_of_measure = models.CharField(max_length=200, choices=(('each', 'each'), ('kg', 'kg'), ('meter', 'meter')), default='each')
    amount = models.DecimalField(max_digits=8, decimal_places=4)
    