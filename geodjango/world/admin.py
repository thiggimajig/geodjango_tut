from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import AirbnbListings #WorldBorder, 
# Register your models here.
# adapted from realpython tutorial
# @admin.register(WorldBorder)
# class WorldBorderAdmin(OSMGeoAdmin):
#     list_display = ('name', 'area')
#from actual geodjango tutorial
# admin.site.register(WorldBorder, admin.GeoModelAdmin)
admin.site.register(AirbnbListings, OSMGeoAdmin)

