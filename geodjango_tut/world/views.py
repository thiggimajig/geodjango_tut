#!/usr/bin/env python3
#where stuff happens functions happen on data from database from models.py
from django.shortcuts import render
from django.views import generic
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance
#not sure but having issues relatively importing.. .maybe when server is down?
# from .models import AirbnbListings 
# from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# import folium
import sys
import os
function_path = os.path.abspath('/Users/stateofplace/new_codes/geodjango_tut/geodjango/world/')
sys.path.append(function_path)
data_path = os.path.abspath('/Users/stateofplace/new_codes/geodjango_tut/geodjango/world/data/')
sys.path.append(data_path)
from . import policy_functions as pf
from . import config_global as config
# from . import popup_html as popup_html

#change it to startingmap
def censusmap(request):
    #create map
    map = config.census_map #change this to the choropleth
    #tried to make it faster by loading database upfront in config global
    # maps = pf.getbubmaps()
    # map = maps[4]
    pop_tot, build_tot, units_tot,homeowners_tot,renters_tot , percentage_rent = pf.load_census_csv_data()
    # # create html version of map
    map = map._repr_html_()
    #coords = [(lat for i in names) , (long for i in names)]
    return render(request,'maps/census_map.html',{'map':map,'pop_tot':pop_tot,'build_tot':build_tot,'units_tot':units_tot,'homeowners_tot':homeowners_tot,'renters_tot':renters_tot,'percentage_rent':percentage_rent })


def policyexplorer(request):
    map = config.map_orig
    #tried to make it faster by loading database upfront in config global
    # maps = pf.getbubmaps()
    # map = maps[0]
    map = map._repr_html_()
    stats_on_air = pf.get_stats()
    tot_listings = stats_on_air[0]
    tot_beds = stats_on_air[1] 
    return render(request,"maps/policy_explorer.html", {'map':map, 'tot_listings':tot_listings, 'tot_beds':tot_beds}) 

# starting_map(original_airbnb_map, stats)
def policyone(request):
    map = config.map_1
    #tried to make it faster by loading database upfront in config global
    # maps = pf.getbubmaps()
    # map = maps[1]
    list_of_updated_stats = pf.get_updated_stats()
    pol1_stats = list_of_updated_stats[0]
    count_listings_effected, count_bedrooms_effected, percentage_effected, percentage_bed_effected = pol1_stats
    # # create html version of map
    map = map._repr_html_()
    # return render(request, "maps/policy1.html",{'allpoints':allpoints,'map':map, 'stats': stats, 'no_permit':no_permit, 'host_count_unique': host_count_unique, 'untaxed_revenue': untaxed_revenue, 'centro_count':centro_count, 'bedroom_count':bedroom_count, 'avg_price': avg_price, 'percent_entire': percent_entire})
    return render(request, "maps/policy1.html",{'map':map, 'count_listings_effected': count_listings_effected, 'count_bedrooms_effected':count_bedrooms_effected, 'percentage_effected':percentage_effected,'percentage_bed_effected':percentage_bed_effected })
# policyone(map_1)

def policytwo(request):
    map = config.map_2
    #tried to make it faster by loading database upfront in config global
    # maps = pf.getbubmaps()
    # map = maps[2]
    list_of_updated_stats = pf.get_updated_stats()
    pol2_stats = list_of_updated_stats[1]
    count_listings_effected, count_bedrooms_effected, percentage_effected, percentage_bed_effected = pol2_stats
    # # create html version of map
    map = map._repr_html_()
    #'no_permit':no_permit, 'host_count_unique': host_count_unique, 'untaxed_revenue': untaxed_revenue, 'centro_count':centro_count, 'bedroom_count':bedroom_count, 'avg_price': avg_price, 'percent_entire': percent_entire
    return render(request, "maps/policy2.html",{'map':map, 'count_listings_effected': count_listings_effected, 'count_bedrooms_effected':count_bedrooms_effected, 'percentage_effected':percentage_effected,'percentage_bed_effected':percentage_bed_effected})

def policythree(request):
#create map
    map = config.map_3
    #tried to make it faster by loading database upfront in config global
    # maps = pf.getbubmaps()
    # map = maps[3]
    list_of_updated_stats = pf.get_updated_stats()
    pol3_stats = list_of_updated_stats[2]
    count_listings_effected, count_bedrooms_effected, percentage_effected, percentage_bed_effected = pol3_stats
    # # create html version of map
    map = map._repr_html_()
    return render(request, "maps/policy3.html",{'map':map, 'count_listings_effected': count_listings_effected, 'count_bedrooms_effected':count_bedrooms_effected, 'percentage_effected':percentage_effected,'percentage_bed_effected':percentage_bed_effected})

# def timelapse(request):
#     return render(request, "maps/timelapse.html")
#non map templates
# def quiz(request):
#     return render(request, "non_maps/quiz.html")
def terms(request):
    return render(request, "non_maps/terms.html")
def about(request):
    return render(request, "non_maps/about.html")
def organize(request):
    return render(request, "non_maps/organize.html")
def method(request):
    return render(request, "non_maps/methodology.html")
# other functions
# def index(request):
#      #create map
#     map = folium.Map(location=[43.7696, 11.2558], tiles='CartoDB Positron', zoom_start=15)
#     #styles of map
#     folium.raster_layers.TileLayer('OpenStreetMap').add_to(map)
#     folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
#     folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
#     folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
#     folium.LayerControl().add_to(map)    
#     allpoints=AirbnbListings.objects.all()
#     names=[i for i in allpoints]
#     no_permit = 0
#     host_count = {}
#     untaxed_revenue = 0
#     centro_count = 0
#     bedroom_count = 0
#     avg_price = 0
#     percent_entire = 0
#     for i in names:
#         html = pf.popup_html(i)
#         folium.Circle([i.latitude, i.longitude], radius=4, color = "blue",opacity=.2, fill = True, fill_opacity = .1, fill_color="blue", tooltip=html, popup=html).add_to(map) 
#         if i.has_liscense == 0:
#             no_permit +=1
#             untaxed_revenue += i.rounded_revenue
#         if i.host_id not in host_count:
#             host_count[i.host_id] = 1
#         else:
#             host_count[i.host_id] += 1
#         if i.neighbourhood_cleansed == 'Centro Storico':
#             centro_count +=1
#         bedroom_count += i.bedrooms
#         avg_price += i.price
#         if i.room_type == 'Entire home/apt':
#             percent_entire+=1 

#     avg_price = avg_price / len(names) 
#     avg_price = round(avg_price,2)
#     percent_entire = (percent_entire / len(names) ) * 100  
#     percent_entire = round(percent_entire)
#     untaxed_revenue = round(untaxed_revenue, 2)
#     host_count_unique = len(host_count)

#     stats = 78723
     
#     # # create html version of map
#     map = map._repr_html_()
    
#     return render(request, "includes/index.html",{'allpoints':allpoints,'map':map, 'stats': stats, 'no_permit':no_permit, 'host_count_unique': host_count_unique, 'untaxed_revenue': untaxed_revenue, 'centro_count':centro_count, 'bedroom_count':bedroom_count, 'avg_price': avg_price, 'percent_entire': percent_entire})

