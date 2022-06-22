from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import AirbnbListings

#AugmentedAirbnbListings #WorldBorder, 
# Register your models here.
# adapted from realpython tutorial
# @admin.register(WorldBorder)
# class WorldBorderAdmin(OSMGeoAdmin):
#     list_display = ('name', 'area')
#from actual geodjango tutorial
# admin.site.register(WorldBorder, admin.GeoModelAdmin)
#AirbnbListings issue with reading new file into databse, headers csvimport so renaming model
admin.site.register(AirbnbListings, OSMGeoAdmin)

# class import_export.admin.ImportMixin
#     from_encoding= 'utf-8'

