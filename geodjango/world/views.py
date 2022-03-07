from django.shortcuts import render
from django.views import generic
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance
from .models import AirbnbListings
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import folium
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

def index(request):
    return render(request, "index.html")

def map(request):
    m = folium.Map()
    # m.save("map_firenze.html")
    # name = "Taylor"
    context = {
        # 'name': name
        'm': m,
    }
    return render(request, "map.html", context) #{'allpoints':queryset,'name':name,'lat':lat,'long':long}

def listings_map(request):
    all_listings = AirbnbListings.objects.all()
    return render (request, 'map_firenze.html', {'all_listings': all_listings})
