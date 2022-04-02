#where stuff happens functions happen on data from database from models.py
from django.shortcuts import render
from django.views import generic
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance
#not sure but having issues relatively importing.. .maybe when server is down?
from .models import AirbnbListings 
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import folium
import sys
import os
function_path = os.path.abspath('/Users/stateofplace/new_codes/geodjango_tut/geodjango/world/')
sys.path.append(function_path)
data_path = os.path.abspath('/Users/stateofplace/new_codes/geodjango_tut/geodjango/world/data/')
sys.path.append(data_path)
from . import policy_functions as pf

#this one allpoints is working so lets go with it
def allpoints(request):
    #create map
    map = folium.Map(location=[43.7696, 11.2558], zoom_start=15)
    # folium.Marker(location=[]).add_to(map)
    #styles of map
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.LayerControl().add_to(map)    
    allpoints=AirbnbListings.objects.all()
    # print(type(allpoints))
    names=[i for i in allpoints]
    # name=[i.name for i in names]
    # price = [i.price for i in names]
    # lat = [i.latitude for i in names]
    # long = [i.longitude for i in names]
    for i in names:
        marker = [i.latitude, i.longitude]
        folium.CircleMarker(location=marker, tooltip=i.name, popup=i.price).add_to(map)
    #create html version of map
    map = map._repr_html_()
    #coords = [(lat for i in names) , (long for i in names)]
    return render(request,'allpoints.html',{'allpoints':allpoints,'map':map})
    #(request, template.html, {variables to pass through})
def starting_map(request):
    # should be able to access ALL variables from policy_functions... so will just display that map here
    # just need to figure out the import issue 
    #then in dashboard it'll use this map variable specific to each template... perfect 
    getmapstuple = pf.getbubmaps()
    map_orig = getmapstuple[0]
    # map = pf.bub_map 
    # map = map._repr_html_()
    # stats = [1,2,3]
    return render(request,"maps/starting_map.html", {"map":map_orig}) #{"originalmap":map, "stats": stats}
# starting_map(original_airbnb_map, stats)
def policyone(request):
    getmapstuple = pf.getbubmaps()
    map_orig = getmapstuple[0]
    map_1 = getmapstuple[1]
    # updatedmap.save(data_path + '/Out_Map/test.html')
    return render(request,"maps/policy1.html", {"map":map_orig, "updatedmap": map_1})
def policytwo(request):
    getmapstuple = pf.getbubmaps()
    map_orig = getmapstuple[0]
    map_2 = getmapstuple[2]
    return render(request,"maps/policy2.html", {"map":map_orig, "updatedmap": map_2})
def policythree(request):
    getmapstuple = pf.getbubmaps()
    map_orig = getmapstuple[0]
    map_3 = getmapstuple[3]
    return render(request,"maps/policy3.html", {"map":map_orig, "updatedmap": map_3})

# other functions
def index(request):
    return render(request, "index.html")

def policy(request):
    return render(request,"policy.html") #{"updated_map":updated_map} #"policy4_df0_funct_map.html"