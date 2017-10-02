import datetime
from decimal import Decimal
from django.db.utils import IntegrityError

from retail.forecast.models import MerchWeek, ProductForecast
from retail.product.models import ProductCategory, Product, ProductOffering, SupplierProduct


def import_product_line(line, count, products):
    """
    Item,BUDesc,Department Desc,Sub Dept Desc,Fineline Desc,Item Description,Item Full Desc
    170965,HG HARDWARE & GARDEN,01 HARDWARE,0112 CHAIN  WIRE & ROPE,1965 U BOLT,U BOLT 25MM ZP 10PC WARRIOR,170965 U BOLT 25MM ZP 10PC WARRIOR
    """
    row = line.split(',')
    
    type = 'standard'
    idtxt = row[0]
    if idtxt[0] == '-':
        type = 'fractional'
        idtxt = idtxt[1:]
    elif idtxt[0] == '!':
        type = 'kit'
        idtxt = idtxt[1:]
        
    try:
        id = int(idtxt)
    except ValueError:
        print( "Ignoring non-numeric SKU: {}".format(row[0]) )
        return

    department, created = ProductCategory.objects.get_or_create(id=int(row[2][0:2]), name=row[2][3:], level='department')
    sub_department, created = ProductCategory.objects.get_or_create(id=int(row[3][0:4]), name=row[3][5:], level='sub_department')
    fineline, created = ProductCategory.objects.get_or_create(id=int(row[4][0:4]), name=row[4][5:],level='fineline')
        
    try:
        product, created = Product.objects.get_or_create(name=row[5], description=row[6].strip(), code=id, status="active")
        products[id] = product
        if created:
            ProductOffering.objects.get_or_create(product=product, sku=id, type=type, department=department, sub_department=sub_department, fineline=fineline )
            SupplierProduct.objects.get_or_create(product=product, supplier_sku=id)
    except IntegrityError:
        print( "Duplicate product:{}".format(row[0]) )
    
    
def import_date_line(line, count, merch_weeks):
    """
    1|"Wk 1 2015"|"Jul  6 2014"|30/6/2014 0:00:00|6/7/2014 0:00:00
    """
    row = line.split('|')
    
    merch_week_no = row[1].strip('"')
    merch_week = row[2].strip('"')
    start_datetxt = row[3].split('/')
    end_datetxt = row[4].split('/')

    start = datetime.date(day=int(start_datetxt[0]),month=int(start_datetxt[1]),year=int(start_datetxt[2][0:4]))
    end = datetime.date(day=int(end_datetxt[0]),month=int(end_datetxt[1]),year=int(end_datetxt[2][0:4]))
    
    merch_weeks[row[3]], created = MerchWeek.objects.get_or_create(number=merch_week_no, name=merch_week, start=start, end=end )
    
    
def bulk_create(count, records):
    ProductForecast.objects.bulk_create(records)
    print( "Bulk create of {} rows ending in row {}".format(len(records),count))
    return []
    
    
def import_line(line, count, records, products, merch_weeks):
    """
    "M10"|5/10/2015 0:00:00|"082443"|0.29
    """
    row = line.split('|')

    division = row[0].strip('"')
    datetxt = row[1]
    item_code = int(row[2].strip('"'))
    amount = Decimal(row[3])
    
    try:
        product = products[item_code]
    except KeyError:
        product = Product.objects.create(id=item_code, type='standard', name='unknown' )
        products[item_code] = product
        print( "Created unknown product:{}".format(item_code) )
        
    try:
        merch_week = merch_weeks[datetxt]
    except KeyError:
        print( "Unknown merch week:{}".format(datetxt) )
        return records

    forecast = ProductForecast( division=division, merch_week=merch_week, product=product, amount=amount )
    records.append(forecast)
    
    if count % 100000 == 0:
        return bulk_create(count, records)
    return records
    

def doproducts(product_filename):
    products = {}
    for product in Product.objects.all():
        products[product.code] = product

    with open(product_filename) as infile:
        count = 0
        for line in infile:
            count += 1
            if count > 1:
                import_product_line(line, count, products)
                
    print( "Created products" )
    return products
    
    
def doimport(extract_filename="Extract.txt", product_filename="Products.csv", weeks_filename="WeeksAndDates.txt"):
    merch_weeks = {}
    records = []

    products = doproducts(products, product_filename)

    with open(weeks_filename) as infile:
        count = 0
        for line in infile:
            count += 1
            import_date_line(line, count, merch_weeks)
    print( "Created merch weeks" )
            
    with open(extract_filename) as infile:
        count = 0
        for line in infile:
            count += 1
            records = import_line(line, count, records, products, merch_weeks)
        if len(records) > 0:
            records = bulk_create(count, records)
            