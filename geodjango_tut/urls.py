#where you hook it up so urls connects to view which is connected to template and pulling from model 

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

# from django.contrib import admin
from django.contrib.gis import admin
from django.urls import path
from world.views import censusmap, policyexplorer, policyone, policytwo, policythree, about, organize, terms, method

urlpatterns = [
    #maps
    path('florence-housing-census', censusmap, name = 'florence-housing-census'), #this is the landing page template for census
    path('all-airbnbs', policyexplorer, name='all-airbnbs'),  #this is the policy explorer template with all airbnb listings
    path('policy-unlicensed-airbnbs', policyone, name='policy-unlicensed-airbnbs'), #this is policy one implmemented
    path('policy-entire-airbnbs', policytwo, name='policy-entire-airbnbs'), #this is policy two implmemented
    path('policy-multiple-airbnbs', policythree, name='policy-multiple-airbnbs'), #this is policy three implmemented
    
    #nonmap
    # path('quiz', quiz, name='quiz'),
    path('terms', terms, name='terms'), #this is glossary of terms and frequently asked qustions myths 
    path('', about, name='about'), #this is aout this project explaining my program my interest my thesis 
    path('organize', organize, name='organize'), #this will have a page explaining global movement, and link to IA
    path('methodology', method, name ='method'), #this will link to calculations on fees, taxes, occupancy, days, revenue, muit listing, scraped data
    #random ones
    # path('', about, name='index'), #for the sake of speed making this function about for now should change to allpoints later OR an explanatory page 
    path('admin/', admin.site.urls)
    # path('timelapse', timelapse, name='timelapse'),
    # listings/ (can be whatever you want the url to be), listings_map (function name in view), 
]
