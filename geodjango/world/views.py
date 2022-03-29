#where stuff happens functions happen on data from database from models.py
from django.shortcuts import render
from django.views import generic
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance
from .models import AirbnbListings
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .policy_functions import stats, updated_stats, ltr_stats, feetax_stats, original_airbnb_map, updated_airbnb_map 
import folium
import pandas as pd
import numpy as np
import statistics as st
import matplotlib as plt
# Create your views here. 
# following this tutorial https://python.plainenglish.io/build-geodjango-webapp-to-store-and-query-locations-91637d485a37
#remember exchanged points for AirbnbListings and description for price

#this one allpoints is working so lets go with it
def allpoints(request):
    #create map
    map = folium.Map(location=[43.7696, 11.2558], zoom_start=7)
    # folium.Marker(location=[]).add_to(map)
    #styles of map
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.LayerControl().add_to(map)    
    allpoints=AirbnbListings.objects.all()
    print(type(allpoints))
    names=[i for i in allpoints]
    name=[i.name for i in names]
    price = [i.price for i in names]
    lat = [i.latitude for i in names]
    long = [i.longitude for i in names]
    for i in names:
        marker = [i.latitude, i.longitude]
        folium.CircleMarker(location=marker, tooltip=i.name, popup=i.price).add_to(map)
    #create html version of map
    map = map._repr_html_()
    #coords = [(lat for i in names) , (long for i in names)]
    return render(request,'allpoints.html',{'allpoints':allpoints,'name':name, 'price':price, 'map':map, 'lat':lat,'long':long})
    #(request, template.html, {variables to pass through})
def index(request):
    return render(request, "index.html")

def policy(request):
    #TODO for later if we think we want to... or just import the df0... then do the map creation here
    # policy1_df0 = (df0.loc[df0['has_liscense'] == 0])
    # updated_bub_map = folium.Map(location=[mapdf.latitude.mean(),mapdf.longitude.mean()], zoom_start=12, control_scale=True, tiles=tileinfo, attr=attribinfo) 
    # folium.LayerControl().add_to(updated_bub_map)
    # for index, location_info in datadf.iterrows():
    #     folium.CircleMarker([location_info["latitude"],location_info["longitude"]], radius=2, color="crimson", fill=True, fill_color ="crimson",  popup="name: <br>" + str((location_info["name"])) + " hostname: <br> " + str(location_info["host_name"]) + " Commercial Property : <br> " + str(location_info["commercial"]) + " Price: <br>" + str(location_info["price"]), tooltip="yearly revenue: " + str(location_info["rounded_revenue"])).add_to(updated_bub_map)
    # updated_map = 'unsure
    return render(request,"policy.html") #{"updated_map":updated_map} #"policy4_df0_funct_map.html"

#ok let's make one policy def where we make all the new dataframes
#then a separate def for each map creation manipulation of the dataframes 

def policyone(request):
    return render(request,"mvp_temps/policy1.html")
def policytwo(request):
    return render(request,"mvp_temps/policy2.html")
def policythree(request):
    return render(request,"mvp_temps/policy3.html")
def starting_map(request):
    return render(request,"mvp_temps/starting_map.html")

def map(request):
    map = folium.Map(location=[43.7696, 11.2558], zoom_start=10)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.LayerControl().add_to(map)   
    map = map._repr_html_()
    # m = folium.Map()
    # # m.save("map_firenze.html")
    # # name = "Taylor"
    context = {
        # 'name': name
        'm': map,
    }
    return render(request, "map.html", context) #{'allpoints':queryset,'name':name,'lat':lat,'long':long}

def listings_map(request):
    all_listings = AirbnbListings.objects.all()
    return render (request, 'map_firenze.html', {'all_listings': all_listings})
