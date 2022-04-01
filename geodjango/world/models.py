#where it all starts, uploading data into database via a model
#TODO figure out if its best practice to keep my processing and policy functions separate...when do i import them into the model? should i make a new app for that? 
# from django.db import models
from django.contrib.gis.db import models
# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models
#headers listing_number,id,listing_url,name,host_id,host_name,host_since,host_location,host_total_listings_count,neighbourhood_cleansed,latitude,longitude,room_type,accommodates,bedrooms,price,availability_30,availability_60,availability_90,availability_365,number_of_reviews_ltm,number_of_reviews_l30d,license,instant_bookable,calculated_host_listings_count,reviews_per_month,days_rented,rounded_revenue,is_hotel,is_entire,many_listings,only_1_listing,only_2_listings,host_florence,has_liscense,is_instant_bookable,global_total_listings,dist_duomo
# This is an auto-generated Django model module created by ogrinspect.
class AirbnbListings(models.Model): #issues here ... 
# Regular Django fields corresponding to the attributes in the IA csv file
    listing_number = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    listing_url = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    host_id = models.IntegerField()
    host_name = models.CharField(max_length=1000)
    host_since = models.CharField(max_length=100)
    host_location = models.CharField(max_length=100)
    host_total_listings_count = models.IntegerField()
    neighbourhood_cleansed = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    room_type = models.CharField(max_length=100)
    accommodates = models.IntegerField()
    bedrooms = models.IntegerField()
    price = models.FloatField()
    availability_30 = models.IntegerField()
    availability_60 = models.IntegerField()
    availability_90 = models.IntegerField()
    availability_365 = models.IntegerField()
    number_of_reviews_ltm = models.IntegerField()
    number_of_reviews_l30d = models.IntegerField()
    license = models.CharField(max_length=100)
    instant_bookable = models.CharField(max_length=10)
    calculated_host_listings_count = models.IntegerField()
    reviews_per_month = models.FloatField()
    days_rented = models.FloatField()
    rounded_revenue = models.FloatField()
    is_hotel = models.IntegerField()
    is_entire = models.IntegerField()
    many_listings = models.IntegerField()
    only_1_listing = models.IntegerField()
    only_2_listings = models.IntegerField()
    host_florence = models.IntegerField()
    has_liscense = models.IntegerField()
    is_instant_bookable = models.IntegerField()
    global_total_listings = models.IntegerField()
    dist_duomo = models.FloatField()
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    #could be points, line, polygon, multipolygon, raster etc 
    geom = models.PointField()
## Auto-generated `LayerMapping` dictionary for AirbnbListings model
augmented_airbnblistings_mapping = {
    'listing_number': 'listing_number',
    'id': 'id',
    'listing_url': 'listing_url',
    'name': 'name',
    'host_id': 'host_id',
    'host_name': 'host_name',
    'host_since': 'host_since',
    'host_location': 'host_location',
    'host_total_listings_count': 'host_total_listings_count',
    'neighbourhood_cleansed': 'neighbourhood_cleansed',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'room_type': 'room_type',
    'accommodates': 'accommodates',
    'bedrooms': 'bedrooms',
    'price': 'price',
    'availability_30': 'availability_30',
    'availability_60': 'availability_60',
    'availability_90': 'availability_90',
    'availability_365': 'availability_365',
    'number_of_reviews_ltm': 'number_of_reviews_ltm',
    'number_of_reviews_l30d': 'number_of_reviews_l30d',
    'license': 'license',
    'instant_bookable': 'instant_bookable',
    'calculated_host_listings_count': 'calculated_host_listings_count',
    'reviews_per_month': 'reviews_per_month',
    'geom': ['latitude', 'longitude'],
}
#define geographic models
# class WorldBorder(models.Model):
#     # Regular Django fields corresponding to the attributes in the
#     # world borders shapefile.
#     name = models.CharField(max_length=50)
#     area = models.IntegerField()
#     pop2005 = models.IntegerField('Population 2005')
#     fips = models.CharField('FIPS Code', max_length=2, null=True)
#     iso2 = models.CharField('2 Digit ISO', max_length=2)
#     iso3 = models.CharField('3 Digit ISO', max_length=3)
#     un = models.IntegerField('United Nations Code')
#     region = models.IntegerField('Region Code')
#     subregion = models.IntegerField('Sub-Region Code')
#     lon = models.FloatField()
#     lat = models.FloatField()

#     # GeoDjango-specific: a geometry field (MultiPolygonField)
#     mpoly = models.MultiPolygonField()

#     # Returns the string representation of the model.
#     def __str__(self):
#         return self.name

#not sure why we want to add this here.. from the script ogrinspect..oh it takes a shapefile and you give it a model name got it
# This is an auto-generated Django model module created by ogrinspect.
# from django.contrib.gis.db import models


# class WorldBorder(models.Model):
#     fips = models.CharField(max_length=2)
#     iso2 = models.CharField(max_length=2)
#     iso3 = models.CharField(max_length=3)
#     un = models.IntegerField()
#     name = models.CharField(max_length=50)
#     area = models.IntegerField()
#     pop2005 = models.BigIntegerField()
#     region = models.IntegerField()
#     subregion = models.IntegerField()
#     lon = models.FloatField()
#     lat = models.FloatField()
#     geom = models.PolygonField()