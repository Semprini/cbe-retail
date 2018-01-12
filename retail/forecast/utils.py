import sys, traceback
import datetime
from decimal import Decimal
from time import sleep

from django.db.utils import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections

from cbe.supplier_partner.models import Supplier
from cbe.location.models import Province, Location
from retail.store.models import Store
from retail.forecast.models import MerchWeek, MerchDate, ProductForecast, ProductSaleWeek
from retail.product.models import ProductCategory, Product, ProductOffering, SupplierProduct, ProductStock
from retail.sale.models import SalesChannel


def yyyymmdd_to_date(datetxt):
    return datetime.date(day=int(datetxt[6:8]), month=int(datetxt[4:6]), year=int(datetxt[:4] ) )


def import_store_line(line):
    """
    Store_code,Store_description,Store,              Class,Store_opening_date,Area_code,Area_description,POSTCODE,Island,Store_urban_flag
    0          1                 2                   3     4                  5         6                7        8      9
    A3,        Ashby's Mitre 10, A3 Ashby's Mitre 10,M10,  0,                 5  ,      area name tbc,   1234,    NTH,   O
    """    
    row = line.split(',')
    
    try:
        store = Store.objects.get(code=row[0])
    except ObjectDoesNotExist:
        store = Store(code=row[0])
    store.name = row[2]
    store.description = row[1]
    if row[3] == "M10":
        store.store_class = "mitre 10"
    elif row[3] == "MEG":
        store.store_class = "mega"
    elif row[3] == "HAM":
        store.store_class = "hammer"
        
    if row[4] != "0":
        store.opening_date = yyyymmdd_to_date(row[4])
    
    try:
        province = Province.objects.get(code=row[5])
    except ObjectDoesNotExist:
        province = Province(code=row[5])
    province.name = row[6]
    province.save()
    
    if store.location == None:
        location = Location(name="Store location")
    else:
        location = store.location
    location.province = province
    location.postcode = row[7]
    
    if row[8] == "STH":
        location.land_mass = "South Island"
    elif row[8] == "NTH":
        location.land_mass = "North Island"
    
    if row[9] == "O":
        location.type = "Rural"
    else:
        location.type = "Urban"
        
    location.save()
    store.location = location
    store.save()
    
    
def import_product_hierarchy_line(line):
    """
    DIVISION|CATEGORY|DEPARTMENT|DEPT_00001  |SUB_D00001|SUB_D00002|FINEL00001|FINEL00002
    "RD"    |"DHW"   |"14"      |"HOUSEWARES"|"1441"    |"CLEANING"|"3462"    |"DAMP CONTROL"
    """
    row = line.strip('\n').split('|')
    
    division_codes = {'RD':1,'HG':2,'OT':3,'BP':4,}
    try:
        division = ProductCategory.objects.get(name=row[0].strip('"'), level='division')
    except ObjectDoesNotExist:
        division = ProductCategory(name=row[0].strip('"'), level='division')
    division.code=division_codes[row[0].strip('"')]
    division.save()
    
    try:
        category = ProductCategory.objects.get(name=row[1].strip('"'), level='category')
    except ObjectDoesNotExist:
        category = ProductCategory(name=row[1].strip('"'), level='category')
        category.code=100001+ProductCategory.objects.filter(level='category').count()
    category.parent=division
    category.save()
    
    try:
        department = ProductCategory.objects.get(code=int(row[2].strip('"')), level='department')
    except ObjectDoesNotExist:
        department = ProductCategory(code=int(row[2].strip('"')), level='department')
    department.parent=category
    department.name=row[3].strip('"')
    department.save()
        
    try:
        sub_department = ProductCategory.objects.get(code=int(row[4].strip('"')), level='sub_department')
    except ObjectDoesNotExist:
        sub_department = ProductCategory(code=int(row[4].strip('"')), level='sub_department')
    sub_department.parent=department
    sub_department.name=row[5].strip('"')
    sub_department.save()

    try:
        fineline = ProductCategory.objects.get(code=int(row[6].strip('"')), level='fineline')
    except ObjectDoesNotExist:
        fineline = ProductCategory(code=int(row[6].strip('"')), level='fineline')
    fineline.parent=sub_department
    fineline.name=row[7].strip('"')
    fineline.save()
    
    
# def import_product_line(line, count, products):
    # """
    # Item,BUDesc,Department Desc,Sub Dept Desc,Fineline Desc,Item Description,Item Full Desc
    # 170965,HG HARDWARE & GARDEN,01 HARDWARE,0112 CHAIN  WIRE & ROPE,1965 U BOLT,U BOLT 25MM ZP 10PC WARRIOR,170965 U BOLT 25MM ZP 10PC WARRIOR
    # """
    # row = line.split(',')
    
    # type = 'standard'
    # idtxt = row[0]
    # if idtxt[0] == '-':
        # type = 'fractional'
        # idtxt = idtxt[1:]
    # elif idtxt[0] == '!':
        # type = 'kit'
        # idtxt = idtxt[1:]
        
    # try:
        # id = int(idtxt)
        # if type == 'fractional':
            # id = 100000000 + id
        # elif type == 'kit':
            # id = 200000000 + id
    # except ValueError:
        # print( "Ignoring non-numeric SKU: {}".format(row[0]) )
        # return

    # department, created = ProductCategory.objects.get_or_create(code=int(row[2][0:2]), name=row[2][3:], level='department')
    # sub_department, created = ProductCategory.objects.get_or_create(code=int(row[3][0:4]), name=row[3][5:], level='sub_department')
    # fineline, created = ProductCategory.objects.get_or_create(code=int(row[4][0:4]), name=row[4][5:],level='fineline')
        
    # try:
        # product, created = Product.objects.get_or_create(name=row[5], description=row[6].strip(), code=id, status="active")
        # products[id] = product
        # if created:
            # ProductOffering.objects.get_or_create(product=product, sku=id, type=type, department=department, sub_department=sub_department, fineline=fineline )
            # SupplierProduct.objects.get_or_create(product=product, supplier_sku=id)
    # except IntegrityError:
        # print( "Duplicate product:{}".format(row[0]) )
    

def import_product_line2(line, channels):
    """
    ZMMDEL|ITEM    |ZMMLOK|ZMMDES                              |ZMMDE2|ZMMDPT|ZMMFIN|ZMMBC|ZMMPNA         |SUPPNO|ZMMSDC|ZMMBRA|ZMMUOM|ZMMPKS|ZMMEOQ|ZMMEQ2|ZMMEQ3|ZMMSL1|ZMMSL2|ZMMSL3|ZMMMS1|ZMMMS2|ZMMMS3|ZMMLDT|ZMMTYP|ZMMTX|ZMMPR1|ZMMPR2|ZMMFGT|ZMMMUP|ZMMRRP|ZMMOP1|ZMMOP2|ZMMORP|ZMICDE     |ZMMCST|ZMMBIN|ZMMPAK|ZMMYTQ|ZMMYTV|ZMMFGA|ZMMFGB|ZMMSGA|ZMMSGB|ZMMALP    |ZMMSU2|ZMMSI2|ZMMCSS|ZMMCSM|ZMMCSL|ZMMIG1|ZMMOLT|ZMMWBI|ZMMWBP|ZMMWBD|ZMMWBF|ZMMPRT|ZMMCRP|ZMMKVI|ZMMIMP|ZMMMEG|ZMMTD1|ZMMTD2|ZMMPLS|ZMMBND|ZMMTRD|ZMMEQS|ZMMBRN|ZMMQB1|ZMMQP1|ZMMQB2|ZMMQP2|ZCRSHS|ZCRSHT|ZCRSWN|ZCRSHM|ZCRHWS|ZCRHNT|ZCRWIN|ZCRHMR|ZCRSEQ|ZMMRR2|ZMMRR3|ZMMMU2|ZMMMU3|ZMMZP2|ZMMZP3|ZMMZF2|ZMMZF3|ZMYSUB|ZMYSTS|ZMYTYP|ZMYBTY|ZMYBPO|ZMYCMA|ZMYKLI|ZMYOSD  |ZMYRED  |ZMYNAD|ZMYMSQ|ZMYLOB|ZMYPLN|ZMYUHT|ZMYUWD|ZMYUDE|ZMYUWT|ZMYIHT|ZMYIWD|ZMYIDE|ZMYIWT|ZMYCHT|ZMYCWD|ZMYCDE|ZMYCWT|ZMYLIS|ZMYRNG|ZMYVEL|ZMYMNL|ZMYMNM|ZMYMNH|ZMYMXL|ZMYMXM|ZMYMXH|ZMYCFD|ZMYQYN|ZMYIGP|ZMYDGS|ZMYSMP|ZMMCD          |ZMMCT  |ZMMCU   |ZMMUD   |ZMMUT   |ZMMUU   |ZMMNCT|ZMMNCU|ZMMRAT|ZMMGTN          |ZMMLKF|ZMMLKU|ZMMLKD|ZMMLKT|ZMMWAR|ZMMWPE|ZMMEQG|ZMMSUS|ZMMFSD  |ZMMREP|ZMMPUO|ZMMPCO|ZMMPCN|ZMMCOO|ZMMSRC|ZMMHER|ZMMSPR|ZMMRA2|ZMMRA3|ZMMRAB|ZMMVAR|ZMMCON|ZMMBAS|ZMMORD|ZMMINV|ZMMDIS|ZMMHR2|ZMMHR3|ZMMHM2|ZMMHM3|ZMMHP2|ZMMHP3|ZMMHF2|ZMMHF3  |ZMMEAD  |ZMMAVL|ZMMCOL|ZMMSIZ
    0      1        2      3                                    4      5      6      7     8               9      10     11     12     13     14     15     16     17     19     19     20     21     22     23     24     25    26     27     28     29     30     31     32     33     34          35     36     37     38     39     40     41     42     43     44         45     46     47     48     49     50     51     52     53     54     55     56     57     58     59     60     61     62     63     64     65     66     67     68     69     70     71     72     73     74     75     76     77     78     79     80     81     82     83     84     85     86     87     88     89     90     91     92     93     94     95     96       97       98     99     100    101    102    103    104    105    106    107    108    109    110    111    112    113    114    115    116    117    118    119    120    121    122    123    124    125    126    127    128             129     130      131      132      133      134    135    136    137              138    139    140    141    142    143    144    145    146      147    148    149    150    151    152    153    154    155    156    157    158    159    160    161    162    163    164    165    166    167    168    169    170    171      172      173    174    175
    "Z"   |"109454"|" "   |"LINE TRIMMER STRGHT SHAFT HOMELITE"|" "   |20    |1250  |"Y"  |"4892210809070"|"RYOB"|" "   |" "   |"EACH"|2.000 |0     |0     |0     |1     |1     |1     |0     |0     |0     |0     |" "   |"G"  |149.00|.00   |" "   |1.5710|234.08|.00   |.00   |.00   |"HLT26SDNB"|149.00|" "   |" "   |0     |.00   |125   |0     |" "   |" "   |"LINE TRI"|" "   |" "   |0     |0     |0     |" "   |" "   |"N"   |" "   |" "   |" "   |" "   |"N"   |"N"   |"N"   |" "   |" "   |" "   |" "   |"N"   |"X"   |0     |" "   |0     |.00   |0     |.00   |0     |0     |0     |0     |" "   |" "   |" "   |"0"   |0     |237.59|241.10|1.5946|1.6181|.00   |.00   |"D"   |"D"   |"2012"|"D"   |"C"   |" "   |" "   |" "   |" "   |20090319|20091102|0     |.000  |"L"   |" "   |.000  |.000  |.000  |.000  |.000  |.000  |.000  |.000  |.000  |.000  |.000  |.000  |" "   |0     |"N"   |.00   |.00   |.00   |.00   |.00   |.00   |" "   |"N"   |0     |" "   |.000  |20090319       |114420 |"M60KB" |20170606|161754  |"M60CT1"|.000  |" "   |" "   |"04892210809070"|" "   |" "   |0     |0     |"N"   |.000  |" "   |" "   |20090319|" "   |" "   |" "   |0     |" "   |" "   |"N"   |" "   |" "   |" "   |"N"   |" "   |" "   |" "   |" "   |" "   |" "   |249.06|264.04|1.6715|1.7721|.00   |.00   |"D"   |"D"     |20091102|"N"   |" "   |" "
    """
    row = line.split('|')

    type = 'standard'
    idtxt = row[1].strip('"')
    if idtxt[0] == '-':
        type = 'fractional'
        idtxt = idtxt[1:]
    elif idtxt[0] == '!':
        type = 'kit'
        idtxt = idtxt[1:]

    try:
        id = int(idtxt)
        if type == 'fractional':
            id = 100000000 + id
        elif type == 'kit':
            id = 200000000 + id
    except ValueError:
        print( "Ignoring non-numeric SKU: {}".format(row[1]) )
        return


    try:
        department = ProductCategory.objects.get( level='department', code=int(row[5]) )
    except ObjectDoesNotExist:
        department = ProductCategory.objects.create(level='department', code=int(row[5]), name='un-named dept')

    try:
        sub_department = ProductCategory.objects.get( level='sub_department', code=int(row[89].strip('"')) )
    except ObjectDoesNotExist:
        sub_department = ProductCategory.objects.create(level='sub_department', code=int(row[89].strip('"')), name='un-named sub-dept')

    try:
        fineline = ProductCategory.objects.get( level='fineline', code=int(row[6]) )
    except ObjectDoesNotExist:
        fineline = ProductCategory.objects.create(level='fineline', code=int(row[6]), name='un-named fineline')

    sub_brand = row[11].strip('"').strip(' ')
    brand = row[67].strip('"').strip(' ') 
    unit_of_measure = row[12].strip('"').lower()
    
    if row[4] == '" "':
        name = row[3].strip('"')
    else:
        name = row[4].strip('"')
    
    #try:
    # Get or create product and details
    product, created = Product.objects.get_or_create(code=id)
    product.name = name
    product.tax_code = row[25].strip('"')
    product.brand=brand
    product.sub_brand=sub_brand
    product.range = int(row[115])
    product.dangerous_classification = row[126].strip('"')
    product.relative_importance_index = row[116].strip('"')
    
    excl_val = {' ':'', 'RE':'Retail Exclusive', 'E':'Exclusive', 'P':'Proprietary', 'BTR':'Better', 'BES':'Best', 'BTY':'BTY'}
    product.exclusive = excl_val[row[92].strip('"')]
    
    product.status=row[90].strip('"')
    product.description=row[3].strip('"')
    if row[57] == '"Y"':
        product.core_range = True
    if row[58] == '"Y"':
        product.key_value_item = True
    if row[59] == '"Y"':
        product.impulse_item = True
    if row[146] != '0':
        product.first_sale_date = yyyymmdd_to_date(row[146])
    if row[157] == '"Y"':
        product.core_abc = True
    # TODO: 2nd loop to set Parents
    product.save()

    # Get or create offering and details
    po, created = ProductOffering.objects.get_or_create(product=product, sku=id, type=type, department=department, sub_department=sub_department, fineline=fineline, barcode=row[8].strip('"') )
    if row[52] != '"N"':
        po.channels.add(channels['Web'])
    
    # Get or supplier product and details
    try:
        supplier = Supplier.objects.get(code=row[9].strip('"'))
    except ObjectDoesNotExist:
        supplier = Supplier.objects.create(code=row[9].strip('"'),name='unnamed supplier')
    
    try:
        sp = SupplierProduct.objects.get(supplier_sku=row[34].strip('"'), supplier=supplier)
    except ObjectDoesNotExist:
        sp = SupplierProduct.objects.create(product=product, supplier_sku=row[34].strip('"'), supplier=supplier)
    sp.unit_of_measure=unit_of_measure
    sp.cost_price = Decimal(row[35])
    sp.reccomended_retail_price = Decimal(row[30])
    sp.reccomended_markup = Decimal(row[29])
    sp.carton_quantity = Decimal(row[13])
    sp.quantity_break1 = Decimal(row[68])
    sp.quantity_price1 = Decimal(row[69])
    sp.quantity_break2 = Decimal(row[70])
    sp.quantity_price2 = Decimal(row[71])
    
    if len(row[98]) == 8:
        sp.next_available_date = yyyymmdd_to_date(row[98])
    sp.save()
    
    # If there is a 2nd supplier then create
    if row[45].strip('"').strip(' ') != "":
        try:
            supplier = Supplier.objects.get(code=row[45].strip('"'))
        except ObjectDoesNotExist:
            supplier = Supplier.objects.create(code=row[45].strip('"'),name='unnamed supplier')
        
        try:
            sp = SupplierProduct.objects.get(supplier_sku=row[46].strip('"'), supplier=supplier)
        except ObjectDoesNotExist:
            sp = SupplierProduct.objects.create(product=product, supplier_sku=row[46].strip('"'), supplier=supplier, unit_of_measure=unit_of_measure)
        
    return product
    #except IntegrityError:
    #    print( "Duplicate product:{}".format(row[1]) )
    
    
def import_week_line(line, count, merch_weeks):
    """
    1|"Wk 1 2015"|"Jul  6 2014"|30/6/2014 0:00:00|6/7/2014 0:00:00
    """
    row = line.split('|')
    year = int(row[0].split(' ')[2])
    
    merch_week_no_txt = row[1].strip('"')
    merch_week_endtxt = row[2].strip('"')
    start_datetxt = row[3].split('/')
    end_datetxt = row[4].split('/')

    start = datetime.date(day=int(start_datetxt[0]),month=int(start_datetxt[1]),year=int(start_datetxt[2][0:4]))
    end = datetime.date(day=int(end_datetxt[0]),month=int(end_datetxt[1]),year=int(end_datetxt[2][0:4]))
    
    merch_weeks[row[3]], created = MerchWeek.objects.get_or_create(number=int(row[0]), year=year, name=merch_week_no_txt, start=start, end=end )


def import_date_line(line):
    """
    ZWEDEL|ZWEDTE  |ZWEDOW              |ZWEWKE  |ZWECWK|ZWECYR|ZWEMWK|ZWEMMT|ZWEMMN|ZWEMQT|ZWEMYR|ZWEWKD|ZWELYR|ZWELMT|ZWELQT|ZWEFYR|ZWEFQT|ZWEFMT|ZWEFMN
    0      1        2                    3        4      5      6      7      8      9      10     11     12     13     14     15     16     17     18
    " "   |20050701|"Friday 1 July 2005"|20050703|26    |2005  |52    |12    |"June"|4     |2005  |"Y"   |2006  |4     |2     |2006  |1     |1     |"July"
    """
    row = line.split('|')
    
    date = yyyymmdd_to_date(row[1])
    datetxt = row[2]

    week_end = yyyymmdd_to_date(row[3])
    week_no = row[4]
    year = row[5]

    merch_week_no = int(row[6])
    merch_week_month = row[7]
    merch_week_year = int(row[10])
    merch_week_name = "Wk {} {}".format(merch_week_no, merch_week_year)
    
    merch_week, created = MerchWeek.objects.get_or_create(number=merch_week_no, month=merch_week_month, year=merch_week_year, name=merch_week_name, calendar_end=week_end, calendar_week_number=week_no )
    merch_date, created = MerchDate.objects.get_or_create(calendar_date=date, calendar_date_txt=datetxt, calendar_week_end=week_end, calendar_week_number=week_no, merch_week=merch_week)
    return merch_date


# def bulk_create(count, records):
    # ProductForecast.objects.bulk_create(records)
    # print( "Bulk create of {} rows ending in row {}".format(len(records),count))
    # return []
    
    
# def import_line(line, count, records, products, merch_weeks):
    # """
    # "M10"|5/10/2015 0:00:00|"082443"|0.29
    # """
    # row = line.split('|')

    # division = row[0].strip('"')
    # datetxt = row[1]
    # item_code = int(row[2].strip('"'))
    # amount = Decimal(row[3])
    
    # try:
        # product = products[item_code]
    # except KeyError:
        # product = Product.objects.create(id=item_code, type='standard', name='unknown' )
        # products[item_code] = product
        # print( "Created unknown product:{}".format(item_code) )
        
    # try:
        # merch_week = merch_weeks[datetxt]
    # except KeyError:
        # print( "Unknown merch week:{}".format(datetxt) )
        # return records

    # forecast = ProductForecast( division=division, merch_week=merch_week, product=product, amount=amount )
    # records.append(forecast)
    
    # if count % 100000 == 0:
        # return bulk_create(count, records)
    # return records


def import_store_sale_week_line(line, products, merch_weeks, stores):
    """
    ZSWST|ZSWIT   |ZSWYR|ZSWW#|ZSWQT|ZSWS$|ZSWC$|ZSWOH |ZSWOO|ZSWRP   |ZSWAV
    Store Item     Year  Week  Quant Sales Cost  stock  onord rrp      av cost 
    0     1        2     3     4     5     6     7      8     9        10
    "A3" |" "     |2012 |43   |.0000|.00  |.00  |.0000 |.0000|.0000   |.00
    "A3" |"!07454"|2012 |1    |.0000|.00  |.00  |2.0000|.0000|199.0000|.00
    """
    row = line.split('|')

    store_code = row[0].strip('"')
    
    type = 'standard'
    idtxt = row[1].strip('"')
    if idtxt[0] == '-':
        type = 'fractional'
        idtxt = idtxt[1:]
    elif idtxt[0] == '!':
        type = 'kit'
        idtxt = idtxt[1:]

    try:
        id = int(idtxt)
        if type == 'fractional':
            id = 100000000 + id
        elif type == 'kit':
            id = 200000000 + id
        try:
            product = products["{}".format(id)]
        except KeyError:
            product = None
    except ValueError:
        product = None

    try:
        merch_week = merch_weeks["{} {}".format(int(row[3]), int(row[2]))] #MerchWeek.objects.get( number=int(row[3]), year=int(row[2]) )
    except KeyError:
        print( "Unknown merch week: {} {}".format(int(row[3]), row[2]) )
        merch_week = None

    try:
        store = stores[row[0].strip('"')] #Store.objects.get( code=row[0].strip('"') )
    except KeyError:
        store = Store.objects.create( code=row[0].strip('"'), name="Unknown store" )
        stores[store.code] = store
    
    end_date = "{}-{}-6".format(row[2], row[3])
    end_date = datetime.datetime.strptime(end_date, "%Y-%W-%w").date()
    
    sale_week = StoreProductSaleWeek( product=product, product_txtid=idtxt, store=store, end_date=end_date)
    sale_week.merch_week=merch_week
    sale_week.quantity = Decimal(row[4])
    sale_week.value = Decimal(row[5])
    sale_week.cost = Decimal(row[6])
    sale_week.on_hand = Decimal(row[7])
    sale_week.on_order = Decimal(row[8])
    sale_week.retail_price = Decimal(row[9])
    sale_week.average_cost = Decimal(row[10])
    #sale_week.save()

    #try:
    #    stock_line = ProductStock.objects.get( product=product, store=store )
    #except ObjectDoesNotExist:
    #    stock_line = ProductStock( product=product, store=store )
    #stock_line.amount = Decimal(row[7])
    #stock_line.retail_price = Decimal(row[9])
    #stock_line.save()
    
    return [sale_week, stores]

    
def import_sale_week_line(line, products, merch_weeks):
    """
    ZSWIT   |ZSWYR|ZSWW#|      ZSWQT|ZSWS$|ZSWC$|ZSWOH |ZSWOO|         |
    Item     Year  Week |count|Quant Sales Cost  stock  onord count soh count sales 
    0        1     2     3     4     5     6      7     8     9         10
    " "     |2012 |43   |     |.0000|.00  |.00  |.0000 |.0000|         |    
    "!07454"|2012 |1    |     |.0000|.00  |.00  |2.0000|.0000|         |    
    
    ZSWIT   |ZSWYR|ZSWW#|STORE00001|AGG_Q00001|AGG_S00001|AGG_C00001|AGG_S00002|AGG_Q00002|STORE00002|STORE00003
    " "     |2015 |42   |8    |.0000|.00  |.00  |.0000 |.0000|0|0
    " "     |2015 |43   |7    |.0000|.00  |.00  |.0000 |.0000|0|0
    
    """
    row = line.split('|')

    type = 'standard'
    idtxt = row[0].strip('"')
    if idtxt[0] == '-':
        type = 'fractional'
        idtxt = idtxt[1:]
    elif idtxt[0] == '!':
        type = 'kit'
        idtxt = idtxt[1:]

    try:
        id = int(idtxt)
        if type == 'fractional':
            id = 100000000 + id
        elif type == 'kit':
            id = 200000000 + id

        try:
            product = products["{}".format(id)]
        except KeyError:
            product = None
    except ValueError:
        product = None


    try:
        merch_week = merch_weeks["{} {}".format(int(row[2]), int(row[1]))] #MerchWeek.objects.get( number=int(row[3]), year=int(row[2]) )
    except KeyError:
        print( "Unknown merch week: {} {}".format(int(row[2]), row[1]) )
        merch_week = None

    end_date = "{}-{}-6".format(row[1], row[2])
    end_date = datetime.datetime.strptime(end_date, "%Y-%W-%w").date()
    
    sale_week = ProductSaleWeek( product=product, product_txtid=idtxt, end_date=end_date)
    sale_week.merch_week=merch_week
    sale_week.store_count=int(row[3])
    sale_week.quantity = Decimal(row[4])
    sale_week.value = Decimal(row[5])
    sale_week.cost = Decimal(row[6])
    sale_week.on_hand = Decimal(row[7])
    sale_week.on_order = Decimal(row[8])
    
    sale_week.store_stock_count = int(row[9])
    sale_week.store_sales_count = int(row[10])
    #sale_week.save()

    #try:
    #    stock_line = ProductStock.objects.get( product=product, store=store )
    #except ObjectDoesNotExist:
    #    stock_line = ProductStock( product=product, store=store )
    #stock_line.amount = Decimal(row[7])
    #stock_line.retail_price = Decimal(row[9])
    #stock_line.save()
    
    return sale_week
    
    
def dostores(filename):
    count = 0
    with open(filename) as infile:
        for line in infile:
            count += 1
            if count > 1:
                import_store_line(line)
    print( "Created {} stores".format(count) )

    
def doproductcategories(filename):
    count = 0
    with open(filename) as infile:
        for line in infile:
            count += 1
            if count > 1:
                import_product_hierarchy_line(line)
    print( "Created {} product categories".format(count) )

    
def doweeklysaleslines(filename):
    sale_lines = []
    products = {}
    merch_weeks = {}
    
    for product in Product.objects.all():
        products[product.code] = product
        
    for merch_week in MerchWeek.objects.all():
        merch_weeks["{} {}".format(merch_week.number,merch_week.year)] = merch_week
        
    with open(filename) as infile:
        count = 0
        for line in infile:
            count += 1
            if count > 1:
                sale_line = import_sale_week_line(line, products, merch_weeks)
                if sale_line:
                    sale_lines.append(sale_line)
                    
            if count%10000 == 0:
                done = False
                retry_count = 0
                while not done and retry_count < 10:
                    try:
                        ProductSaleWeek.objects.bulk_create(sale_lines)
                        sale_lines = []
                        print( "Batch of 10k done. Current count:{}".format(count) )
                        done = True
                    except DatabaseError as err:
                        print( "DATABASE ERROR! Closing unusable connections and retrying shortly. %s"%err )
                        sleep(10)
                        for conn in connections.all():
                            conn.close_if_unusable_or_obsolete()
                        sleep(10)
                        retry_count+=1
                if retry_count >= 10:
                    raise Exception( "FATAL DATABASE ERROR!" )
                    
        
        if len(sale_lines) > 0:
            done = False
            retry_count = 0
            while not done and retry_count < 10:
                try:
                    ProductSaleWeek.objects.bulk_create(sale_lines)        
                    done = True
                except DatabaseError as err:
                    print( "DATABASE ERROR! Closing unusable connections and retrying shortly. %s"%err )
                    sleep(10)
                    for conn in connections.all():
                        conn.close_if_unusable_or_obsolete()
                    sleep(10)
                    retry_count+=1
            if retry_count >= 10:
                raise Exception( "FATAL DATABASE ERROR!" )


                    
    print( "Created {} weekly sale lines".format(count) )    
    
def dostoreweeklysaleslines(filename):
    sale_lines = []
    products = {}
    merch_weeks = {}
    stores = {}
    
    for product in Product.objects.all():
        products[product.code] = product
        
    for merch_week in MerchWeek.objects.all():
        merch_weeks["{} {}".format(merch_week.number,merch_week.year)] = merch_week
        
    for store in Store.objects.all():
        stores[store.code] = store

    with open(filename) as infile:
        count = 0
        for line in infile:
            count += 1
            if count > 1:
                sale_line, stores = import_store_sale_week_line(line, products, merch_weeks, stores)
                if sale_line:
                    sale_lines.append(sale_line)
                    
            if count%10000 == 0:
                done = False
                retry_count = 0
                while not done and retry_count < 10:
                    try:
                        ProductSaleWeek.objects.bulk_create(sale_lines)
                        sale_lines = []
                        print( "Batch of 10k done. Current count:{}".format(count) )
                        done = True
                    except DatabaseError as err:
                        print( "DATABASE ERROR! Closing unusable connections and retrying shortly. %s"%err )
                        sleep(10)
                        for conn in connections.all():
                            conn.close_if_unusable_or_obsolete()
                        sleep(10)
                        retry_count+=1
                if retry_count >= 10:
                    raise Exception( "FATAL DATABASE ERROR!" )
                    
        
        if len(sale_lines) > 0:
            done = False
            retry_count = 0
            while not done and retry_count < 10:
                try:
                    ProductSaleWeek.objects.bulk_create(sale_lines)        
                    done = True
                except DatabaseError as err:
                    print( "DATABASE ERROR! Closing unusable connections and retrying shortly. %s"%err )
                    sleep(10)
                    for conn in connections.all():
                        conn.close_if_unusable_or_obsolete()
                    sleep(10)
                    retry_count+=1
            if retry_count >= 10:
                raise Exception( "FATAL DATABASE ERROR!" )


                    
    print( "Created {} weekly sale lines".format(count) )

    
def domerchdates(filename):
    merch_dates = {}
    for merch_date in MerchDate.objects.all():
        merch_dates[merch_date.calendar_date] = merch_date

    with open(filename) as infile:
        count = 0
        for line in infile:
            count += 1
            if count > 1:
                merch_date = import_date_line(line)
                if merch_date:
                    merch_dates[merch_date.calendar_date] = merch_date
    print( "Created {} merch dates".format(len(merch_dates)) )
    return merch_dates
    
    
# def doproducts(product_filename):
    # products = {}
    # for product in Product.objects.all():
        # products[product.code] = product

    # with open(product_filename) as infile:
        # count = 0
        # for line in infile:
            # count += 1
            # if count > 1:
                # import_product_line(line, count, products)
                
    # print( "Created products" )
    # return products
    

def doproducts2(product_filename, startline=0):
    web_channel, created = SalesChannel.objects.get_or_create(name="Web")
    m10_channel, created = SalesChannel.objects.get_or_create(name="Mitre 10")
    mega_channel, created = SalesChannel.objects.get_or_create(name="Mega")
    hammer_channel, created = SalesChannel.objects.get_or_create(name="Hammer")
    channels = {'Web':web_channel,'Mitre 10':m10_channel, 'Mega':mega_channel, 'Hammer':hammer_channel }
    
    with open(product_filename, encoding = "ISO-8859-1") as infile:
        count = 0
        for line in infile:
            try:
                if count > startline:
                    product = import_product_line2(line, channels)
                count += 1
            except Exception:
                print("Exception in user code on line {}. Data was:".format(count))
                print(line)
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)
            if count%1000==0:
                print( "so far {} products imported".format(count) )
    print( "Imported {} products".format(count) )

    
# def doimport1(extract_filename="Extract.txt", product_filename="Products.csv", weeks_filename="WeeksAndDates.txt"):
    # merch_weeks = {}
    # records = []

    # products = doproducts(products, product_filename)

    # with open(weeks_filename) as infile:
        # count = 0
        # for line in infile:
            # count += 1
            # import_week_line(line, count, merch_weeks)
    # print( "Created merch weeks" )
            
    # with open(extract_filename) as infile:
        # count = 0
        # for line in infile:
            # count += 1
            # records = import_line(line, count, records, products, merch_weeks)
        # if len(records) > 0:
            # records = bulk_create(count, records)
            