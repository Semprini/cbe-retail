import sys, traceback
import datetime
from decimal import Decimal
from time import sleep

from django.db.utils import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections

from cbe.location.models import Province, Location
from cbe.party.models import Organisation
from cbe.resource.models import LogicalResource
from cbe.human_resources.models import Identification, IdentificationType
from cbe.physical_object.models import Structure

from retail.store.models import Store


def yyyymmdd_to_date(datetxt):
    return datetime.date(day=int(datetxt[6:8]), month=int(datetxt[4:6]), year=int(datetxt[:4] ) )


def import_org_line(line):
    """
    static_id,resource_pacsoft_instance_ip_address,owning_organisation_name,Info-only: Current Primary Store Code
    1,        192.168.178.10,                      Ashby's Mitre 10,        A3
    """
    row = line.split(',')
    m10,created = Organisation.objects.get_or_create( name="Mitre 10" )
    
    try:
        org = Organisation.objects.get( enterprise_id=int(row[0]) )
    except ObjectDoesNotExist:
        org = Organisation( enterprise_id=int(row[0]) )
    
    org.name = row[2]
    org.save()
    
    ps,created = LogicalResource.objects.get_or_create( name="Pacsoft {}".format(org.enterprise_id) )
    it,created = IdentificationType.objects.get_or_create( name="IP Address", system=ps, issuer=m10 )
    ids = Identification.objects.filter( identification_type=it, organisation=org, )
    if ids.count() == 0:
        id = Identification( identification_type=it, party=org, )
        ids = [id,]
    ids[0].number = row[1]
    ids[0].save()

    
def doorgs(filename):
    count = 0
    with open(filename) as infile:
        for line in infile:
            count += 1
            if count > 1:
                import_org_line(line)
    print( "Imported {} orgs".format(count) )


def import_store_line(line):
    """
    owning_organisation_static_id, static_store_id, trm_store_code, store_name,           store_type, store_class, store_code_history,current_store_code, current_store_code_start, current_store_code_end, prev1_store_code, prev1_store_start, prev1_store_end, prev2_store_code, prev2_store_start ,prev2_store_end, prev3_store_code, prev3_store_start, prev3_store_end, latitude,   longitude,   address_line_1,             address_line_2, locality, city,             postcode, floor_area, island, trade_area, retail_area,          national_area, ssid,      psk, store_octet, store_subnet
    0                              1                2               3                     4           5            6                  7                   8                         9                       10                11                 12               13                14                 15               16                17                 18               19          20           21                          22              23        24                25        26          27      28          29                    30             31         32   33           34               
    46,                            1,               ABY,            Mitre 10 MEGA Albany, mega,       mega-1,      X51|X26,           X51,                1/12/2014,                ,                       X26,              12/12/2008,        30/11/2014     ,                 ,                   ,               ,                 ,                 ,                 , -36.722206, 174.7062077, 260 Oteha Valley Road Extn,               , Albany,   North Shore City, 0632,     7560,       north,  auckland,   upper ni / north akl, auckland,      ABY Rugged,   , 105,         192.168.105.*
    """
    row = line.split(',')
    m10,created = Organisation.objects.get_or_create( name="Mitre 10" )

    try:
        org = Organisation.objects.get(enterprise_id=int(row[0]))
    except ObjectDoesNotExist:
        print( "Missing Organisation" )
        print( row )
        raise

    try:
        store = Store.objects.get(enterprise_id=int(row[1]))
    except ObjectDoesNotExist:
        store = Store(enterprise_id=int(row[1]))
        
    store.organisation = org
    store.name = row[3]
    store.code = row[7]
    
    if row[4] == "mitre10":
        store.store_type = "mitre 10"
    elif row[4] == "mega":
        store.store_type = "mega"
    elif row[4] == "hammer":
        store.store_type = "hammer"
    elif row[4] == "trade":
        store.store_type = "trade"
    
    store.store_class = row[5]

    if store.location == None:
        location = Location(name="Store location")
    else:
        location = store.location

    location.postcode = row[25]
    
    try:
        location.latitude = Decimal(row[19])
        location.longitude = Decimal(row[20])
    except:
        print("No lat or long: {}".format(row))
    location.address_line1 = row[21]
    location.address_line2 = row[22]
    
    if row[8] == "south":
        location.land_mass = "South Island"
    elif row[8] == "north":
        location.land_mass = "North Island"
        
    location.save()
    store.location = location
    
    store.save()

    try:
        building = store.buildings.get( name="Main Building" )
    except ObjectDoesNotExist:
        building = Structure.objects.create( name="Main Building" )
        store.buildings.add(building)
        
    building.location = location
    building.floor_square_metres = int(row[26])
    building.save()
    
    it,created = IdentificationType.objects.get_or_create( name="Store Code", issuer=m10 )
    try:
        id = Identification.objects.get( identification_type=it, store=store, number=row[7] )
    except ObjectDoesNotExist:
        id = Identification.objects.create( identification_type=it, party_role=store, number=row[7] )
        store.identifiers.add(id)
    if row[8] != "":
        id.valid_from = datetime.datetime.strptime(row[8], "%d/%m/%Y").date()
    id.save()
    
    if row[10] != "":
        try:
            id = Identification.objects.get( identification_type=it, store=store, number=row[10] )
        except ObjectDoesNotExist:
            id = Identification.objects.create( identification_type=it, party_role=store, number=row[10] )
            store.identifiers.add(id)
        id.valid_from = datetime.datetime.strptime(row[11], "%d/%m/%Y").date()
        id.valid_to = datetime.datetime.strptime(row[12], "%d/%m/%Y").date()
        id.save()
        

def dostores(filename):
    count = 0
    with open(filename) as infile:
        for line in infile:
            count += 1
            if count > 1:
                import_store_line(line)
    print( "Imported {} stores".format(count) )
    
    
def import_store_line_as400(line):
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
        store.store_type = "mitre 10"
    elif row[3] == "MEG":
        store.store_type = "mega"
    elif row[3] == "HAM":
        store.store_type = "hammer"
        
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
    
    
def dostores_as400(filename):
    count = 0
    with open(filename) as infile:
        for line in infile:
            count += 1
            if count > 1:
                import_store_line_as400(line)
    print( "Imported {} stores".format(count) )

    
