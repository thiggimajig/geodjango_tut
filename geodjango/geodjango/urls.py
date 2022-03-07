"""geodjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#following this tutorial https://python.plainenglish.io/build-geodjango-webapp-to-store-and-query-locations-91637d485a37
# remember exchanged points for AirbnbListings and description for price 

# from django.contrib import admin
from django.contrib.gis import admin
from django.urls import path
from world.views import allpoints, map, index, listings_map

urlpatterns = [
    path('admin/', admin.site.urls),
    path('allpoints', allpoints, name = 'allpoints'),
    path('index', index, name='index'),
    path('map', map, name='map'),
    path('world', listings_map, name = 'listings-map')
    #path('', views.AirbnbListings.as_view())
    # path('map/', )
]
