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
# from . import popup_html as popup_html

#this one allpoints is working so lets go with it
def allpoints(request):
    #create map
    map = folium.Map(location=[43.7696, 11.2558], tiles='CartoDB Positron', zoom_start=15)
  

    #styles of map
    folium.raster_layers.TileLayer('OpenStreetMap').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.LayerControl().add_to(map)    
    allpoints=AirbnbListings.objects.all()
    names=[i for i in allpoints]
    # name=[i.name for i in names]
    # price = [i.price for i in names]
    # lat = [i.latitude for i in names]
    # long = [i.longitude for i in names]
    # for i in names:
    #     marker = [i.latitude, i.longitude]
    #     folium.CircleMarker(location=marker, tooltip=i.name, popup=i.price).add_to(map) #popup=i.price
    for i in names:
        html = pf.popup_html(i)
        # marker = [i.latitude, i.longitude]
        folium.Circle([i.latitude, i.longitude], radius=4, color = "blue",opacity=.2, fill = True, fill_opacity = .1, fill_color="blue", tooltip=html, popup=html).add_to(map) 
    # # create html version of map
    map = map._repr_html_()
    #coords = [(lat for i in names) , (long for i in names)]
    return render(request,'allpoints.html',{'allpoints':allpoints,'map':map})
    #(request, template.html, {variables to pass through})
def starting_map(request):
    # should be able to access ALL variables from policy_functions... so will just display that map here
    #then in dashboard it'll use this map variable specific to each template... perfect 
    # getmapstuple = pf.getbubmaps()
    # map_orig = getmapstuple[0]
    # # map = pf.bub_map 
    # # map = map._repr_html_()
    # # stats = [1,2,3]
         #create map
    map = folium.Map(location=[43.7696, 11.2558], tiles='CartoDB Positron', zoom_start=15)
    #styles of map
    folium.raster_layers.TileLayer('OpenStreetMap').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.LayerControl().add_to(map)    
    allpoints=AirbnbListings.objects.all()
    names=[i for i in allpoints]
    no_permit = 0
    host_count = {}
    untaxed_revenue = 0
    centro_count = 0
    bedroom_count = 0
    avg_price = 0
    percent_entire = 0
    for i in names:
        html = pf.popup_html(i)
        folium.Circle([i.latitude, i.longitude], radius=4, color = "blue",opacity=.2, fill = True, fill_opacity = .1, fill_color="blue", tooltip=html, popup=html).add_to(map) 
        if i.has_liscense == 0:
            no_permit +=1
            untaxed_revenue += i.rounded_revenue
        if i.host_id not in host_count:
            host_count[i.host_id] = 1
        else:
            host_count[i.host_id] += 1
        if i.neighbourhood_cleansed == 'Centro Storico':
            centro_count +=1
        bedroom_count += i.bedrooms
        avg_price += i.price
        if i.room_type == 'Entire home/apt':
            percent_entire+=1 

    avg_price = avg_price / len(names) 
    avg_price = round(avg_price,2)
    percent_entire = (percent_entire / len(names) ) * 100  
    percent_entire = round(percent_entire)
    untaxed_revenue = round(untaxed_revenue, 2)
    host_count_unique = len(host_count)

    stats = 78723
     
    # # create html version of map
    map = map._repr_html_()
    
    return render(request, "maps/starting_map.html",{'allpoints':allpoints,'map':map, 'stats': stats, 'no_permit':no_permit, 'host_count_unique': host_count_unique, 'untaxed_revenue': untaxed_revenue, 'centro_count':centro_count, 'bedroom_count':bedroom_count, 'avg_price': avg_price, 'percent_entire': percent_entire})

# starting_map(original_airbnb_map, stats)
def policyone(request):
    # getmapstuple = pf.getbubmaps()
    # map_orig = getmapstuple[0]
    # map_1 = getmapstuple[1]
    # # updatedmap.save(data_path + '/Out_Map/test.html')
             #create map
    map = folium.Map(location=[43.7696, 11.2558], tiles='CartoDB Positron', zoom_start=15)
    #styles of map
    folium.raster_layers.TileLayer('OpenStreetMap').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.LayerControl().add_to(map)    
    allpoints=AirbnbListings.objects.all()
    names=[i for i in allpoints]
    no_permit = 0
    host_count = {}
    untaxed_revenue = 0
    centro_count = 0
    bedroom_count = 0
    avg_price = 0
    percent_entire = 0
    for i in names:
        html = pf.popup_html(i)
        folium.Circle([i.latitude, i.longitude], radius=4, color = "blue",opacity=.2, fill = True, fill_opacity = .1, fill_color="blue", tooltip=html, popup=html).add_to(map) 
        if i.has_liscense == 0:
            no_permit +=1
            untaxed_revenue += i.rounded_revenue
        if i.host_id not in host_count:
            host_count[i.host_id] = 1
        else:
            host_count[i.host_id] += 1
        if i.neighbourhood_cleansed == 'Centro Storico':
            centro_count +=1
        bedroom_count += i.bedrooms
        avg_price += i.price
        if i.room_type == 'Entire home/apt':
            percent_entire+=1 

    avg_price = avg_price / len(names) 
    avg_price = round(avg_price,2)
    percent_entire = (percent_entire / len(names) ) * 100  
    percent_entire = round(percent_entire)
    untaxed_revenue = round(untaxed_revenue, 2)
    host_count_unique = len(host_count)

    stats = 78723
     
    # # create html version of map
    map = map._repr_html_()
    
    return render(request, "maps/policy1.html",{'allpoints':allpoints,'map':map, 'stats': stats, 'no_permit':no_permit, 'host_count_unique': host_count_unique, 'untaxed_revenue': untaxed_revenue, 'centro_count':centro_count, 'bedroom_count':bedroom_count, 'avg_price': avg_price, 'percent_entire': percent_entire})

def policytwo(request):
    # getmapstuple = pf.getbubmaps()
    # map_orig = getmapstuple[0]
    # map_2 = getmapstuple[2]
                 #create map
    map = folium.Map(location=[43.7696, 11.2558], tiles='CartoDB Positron', zoom_start=15)
    #styles of map
    folium.raster_layers.TileLayer('OpenStreetMap').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.LayerControl().add_to(map)    
    allpoints=AirbnbListings.objects.all()
    names=[i for i in allpoints]
    no_permit = 0
    host_count = {}
    untaxed_revenue = 0
    centro_count = 0
    bedroom_count = 0
    avg_price = 0
    percent_entire = 0
    for i in names:
        html = pf.popup_html(i)
        folium.Circle([i.latitude, i.longitude], radius=4, color = "blue",opacity=.2, fill = True, fill_opacity = .1, fill_color="blue", tooltip=html, popup=html).add_to(map) 
        if i.has_liscense == 0:
            no_permit +=1
            untaxed_revenue += i.rounded_revenue
        if i.host_id not in host_count:
            host_count[i.host_id] = 1
        else:
            host_count[i.host_id] += 1
        if i.neighbourhood_cleansed == 'Centro Storico':
            centro_count +=1
        bedroom_count += i.bedrooms
        avg_price += i.price
        if i.room_type == 'Entire home/apt':
            percent_entire+=1 

    avg_price = avg_price / len(names) 
    avg_price = round(avg_price,2)
    percent_entire = (percent_entire / len(names) ) * 100  
    percent_entire = round(percent_entire)
    untaxed_revenue = round(untaxed_revenue, 2)
    host_count_unique = len(host_count)

    stats = 78723
     
    # # create html version of map
    map = map._repr_html_()
    
    return render(request, "maps/policy2.html",{'allpoints':allpoints,'map':map, 'stats': stats, 'no_permit':no_permit, 'host_count_unique': host_count_unique, 'untaxed_revenue': untaxed_revenue, 'centro_count':centro_count, 'bedroom_count':bedroom_count, 'avg_price': avg_price, 'percent_entire': percent_entire})

def policythree(request):
    # getmapstuple = pf.getbubmaps()
    # map_orig = getmapstuple[0]
    # map_3 = getmapstuple[3]
                 #create map
    map = folium.Map(location=[43.7696, 11.2558], tiles='CartoDB Positron', zoom_start=15)
    #styles of map
    folium.raster_layers.TileLayer('OpenStreetMap').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.LayerControl().add_to(map)    
    allpoints=AirbnbListings.objects.all()
    names=[i for i in allpoints]
    no_permit = 0
    host_count = {}
    untaxed_revenue = 0
    centro_count = 0
    bedroom_count = 0
    avg_price = 0
    percent_entire = 0
    for i in names:
        html = pf.popup_html(i)
        folium.Circle([i.latitude, i.longitude], radius=4, color = "blue",opacity=.2, fill = True, fill_opacity = .1, fill_color="blue", tooltip=html, popup=html).add_to(map) 
        if i.has_liscense == 0:
            no_permit +=1
            untaxed_revenue += i.rounded_revenue
        if i.host_id not in host_count:
            host_count[i.host_id] = 1
        else:
            host_count[i.host_id] += 1
        if i.neighbourhood_cleansed == 'Centro Storico':
            centro_count +=1
        bedroom_count += i.bedrooms
        avg_price += i.price
        if i.room_type == 'Entire home/apt':
            percent_entire+=1 

    avg_price = avg_price / len(names) 
    avg_price = round(avg_price,2)
    percent_entire = (percent_entire / len(names) ) * 100  
    percent_entire = round(percent_entire)
    untaxed_revenue = round(untaxed_revenue, 2)
    host_count_unique = len(host_count)

    stats = 78723
     
    # # create html version of map
    map = map._repr_html_()
    
    return render(request, "maps/policy3.html",{'allpoints':allpoints,'map':map, 'stats': stats, 'no_permit':no_permit, 'host_count_unique': host_count_unique, 'untaxed_revenue': untaxed_revenue, 'centro_count':centro_count, 'bedroom_count':bedroom_count, 'avg_price': avg_price, 'percent_entire': percent_entire})

def timelapse(request):
    return render(request, "maps/timelapse.html")
#non map templates
def quiz(request):
    return render(request, "non_maps/quiz.html")
def terms(request):
    return render(request, "non_maps/terms.html")
def about(request):
    return render(request, "non_maps/about.html")
def organize(request):
    return render(request, "non_maps/organize.html")
def method(request):
    return render(request, "non_maps/methodology.html")
# other functions
def index(request):
     #create map
    map = folium.Map(location=[43.7696, 11.2558], tiles='CartoDB Positron', zoom_start=15)
    #styles of map
    folium.raster_layers.TileLayer('OpenStreetMap').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.LayerControl().add_to(map)    
    allpoints=AirbnbListings.objects.all()
    names=[i for i in allpoints]
    no_permit = 0
    host_count = {}
    untaxed_revenue = 0
    centro_count = 0
    bedroom_count = 0
    avg_price = 0
    percent_entire = 0
    for i in names:
        html = pf.popup_html(i)
        folium.Circle([i.latitude, i.longitude], radius=4, color = "blue",opacity=.2, fill = True, fill_opacity = .1, fill_color="blue", tooltip=html, popup=html).add_to(map) 
        if i.has_liscense == 0:
            no_permit +=1
            untaxed_revenue += i.rounded_revenue
        if i.host_id not in host_count:
            host_count[i.host_id] = 1
        else:
            host_count[i.host_id] += 1
        if i.neighbourhood_cleansed == 'Centro Storico':
            centro_count +=1
        bedroom_count += i.bedrooms
        avg_price += i.price
        if i.room_type == 'Entire home/apt':
            percent_entire+=1 

    avg_price = avg_price / len(names) 
    avg_price = round(avg_price,2)
    percent_entire = (percent_entire / len(names) ) * 100  
    percent_entire = round(percent_entire)
    untaxed_revenue = round(untaxed_revenue, 2)
    host_count_unique = len(host_count)

    stats = 78723
     
    # # create html version of map
    map = map._repr_html_()
    
    return render(request, "includes/index.html",{'allpoints':allpoints,'map':map, 'stats': stats, 'no_permit':no_permit, 'host_count_unique': host_count_unique, 'untaxed_revenue': untaxed_revenue, 'centro_count':centro_count, 'bedroom_count':bedroom_count, 'avg_price': avg_price, 'percent_entire': percent_entire})

def policy(request):
    return render(request,"policy.html") #{"updated_map":updated_map} #"policy4_df0_funct_map.html"