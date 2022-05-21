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
from world.views import allpoints, policyone, policy, about, organize, terms, method

urlpatterns = [
    #maps
    path('allpoints', allpoints, name = 'allpoints'),
    # path('startingmap', starting_map, name='startingmap'),
    path('policyone', policyone, name='policyone'),
    # path('policytwo', policytwo, name='policytwo'),
    # path('policythree', policythree, name='policythree'),
    path('policyexplorer', policy, name='policyexplorer'),
    # path('timelapse', timelapse, name='timelapse'),
    #nonmap
    # path('quiz', quiz, name='quiz'),
    path('terms', terms, name='terms'),
    path('about', about, name='about'),
    path('organize', organize, name='organize'),
    path('methodology', method, name ='method'),
    #random ones
    # path('', index, name='index'),
    path('admin/', admin.site.urls)
    # listings/ (can be whatever you want the url to be), listings_map (function name in view), 
]
