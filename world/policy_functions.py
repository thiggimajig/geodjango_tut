#!/usr/bin/env python3
from operator import and_
# import geojson
# import geopandas
import pandas as pd
# import numpy as np
# import statistics as st
# import matplotlib as plt
import folium
# from folium.features import CustomIcon
# import csv
# import geopandas
from IPython.display import display, HTML
# from pathlib import Path 
import os
import sys
from .models import AirbnbListings
# from . import config_global as config

data_path = os.path.abspath('/Users/stateofplace/new_codes/geodjango_tut/geodjango_tut/world/data/')
sys.path.append(data_path)
# sys.path.append("/geodjango/world/data/policy_functions")
#example of absolute path settting for file... 
# dirpath = os.path.dirname(os.path.abspath(__file__))
# chap_dirpath = os.path.join(dirpath, chap_dirpath)


esri = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
attrib = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'

#successfully refactored to pull from database not csv file
#found this from ... https://stackoverflow.com/questions/11697887/converting-django-queryset-to-pandas-dataframe 
#an alternative method # Convert Django's Queryset into a Pandas DataFrame: pricing_dataframe = pd.DataFrame.from_records(prices.values())
#i think i need to use iterator here to help memory issues... 
# star_set = Star.objects.all()
# # The `iterator()` method ensures only a few rows are fetched from
# # the database at a time, saving memory.
# for star in star_set.iterator():
#     print(star.name)
#try using @cached_property
def load_database_data():
    # airbnb_data = AirbnbListings.objects.all().values('id', 'has_liscense', 'days_rented_ltm', 'rounded_revenue_ltm', 'price', 'name', 'host_id', 'bedrooms', 'many_listings', 'availability_365', 'is_hotel', 'host_name', 'commercial', 'is_entire', 'latitude', 'longitude')
    # for listing in airbnb_data.iterator():
    #     df = pd.DataFrame(list(listing))
    #.iterator() tried to see if faster... 
    df = pd.DataFrame(list(AirbnbListings.objects.all().values('effected_by_policy_3','effected_by_policy_2','effected_by_policy_1','host_since','host_total_listings_count','host_florence','reviews_per_month','accommodates','room_type','dist_duomo','id', 'has_liscense', 'neighbourhood_cleansed', 'license','listing_url','days_rented_ltm', 'rounded_revenue_ltm', 'price', 'name', 'host_id', 'bedrooms', 'many_listings', 'availability_365', 'is_hotel', 'host_name', 'commercial', 'is_entire', 'latitude', 'longitude')))
    print("load data base is running")
    return df
#here we create the cleaned dataframe we want having dropped things we don't care about...but that'll change
def clean_dataframe(s):
    columns_df0 = ['effected_by_policy_3','effected_by_policy_2','effected_by_policy_1','host_since','host_total_listings_count','host_florence','reviews_per_month','accommodates','room_type','dist_duomo','neighbourhood_cleansed','license','listing_url' ,'id', 'has_liscense', 'days_rented_ltm', 'rounded_revenue_ltm', 'price', 'name', 'host_id', 'bedrooms', 'many_listings', 'availability_365', 'is_hotel', 'host_name', 'commercial', 'is_entire', 'latitude', 'longitude']
    cleaned_df = s.loc[:,columns_df0]
    # print(cleaned_df.head())
    return cleaned_df
# df0 = clean_dataframe(df)

def load_census_csv_data():
    df_census = pd.read_csv("/Users/stateofplace/new_codes/geodjango_tut/csv/R09_fi_app.csv")
    population = df_census.loc[:, 'P1']
    buildings = df_census.loc[:,'E3']
    units = df_census.loc[:, 'E27']
    homeowners = df_census.loc[:, 'A47']
    renters = df_census.loc[:, 'A46']
    pop_tot = (population.sum())
    build_tot = buildings.sum()
    units_tot = units.sum()
    homeowners_tot = homeowners.sum()
    renters_tot = renters.sum()
    percentage_rent = round(((renters_tot / pop_tot) * 100),2)
    return pop_tot, build_tot, units_tot,homeowners_tot,renters_tot , percentage_rent


#here from that cleaned data frame i make dataframes with data specific for each policy function...
#but i can instead make the dataframes with specific data by looping through the model database data
def create_specific_dataframes(s):
    #policy1 df
    no_lisc_df0 = (s.loc[s['has_liscense'] == 0])
    lisc_df0 = (s.loc[s['has_liscense'] == 1])
    # print(no_lisc_df0.head())
    #policy1 comm df
    comm_no_lisc_df0 = (no_lisc_df0.loc[no_lisc_df0['commercial'] == 1])
    nocomm_no_lisc_df0 = (no_lisc_df0.loc[no_lisc_df0['commercial'] == 0])
    #policy2 df
    entire_df0 = (s.loc[s['is_entire'] == 1])
    not_entire_df0 = (s.loc[s['is_entire'] == 0]) #and (s.loc[s['is_hotel'] == 0]) not entire or hotel is_hotel == 0
     
    #policy3 df
    many_listings_df0 = (s.loc[s['many_listings'] == 1])
    not_many_listings_df0 = (s.loc[s['many_listings'] == 0])

    return no_lisc_df0, lisc_df0, comm_no_lisc_df0, nocomm_no_lisc_df0, entire_df0, not_entire_df0, many_listings_df0, not_many_listings_df0

# policy1_df0, policy1_df0_inverse, policy1_df0_comm, policy1_df0_nocomm, policy2_df0, policy2_df0_inverse, policy3_df0, policy3_df0_inverse = create_specific_dataframes(df0)

#here i create basic stats from the entire data...but if i can loop through all rows in the model i can accomplish this or I can use the new dataframes with the model data if we go that route
def stats(dataframe):
    #calculate stats for given area before any regulation
    fi_stats = []
    count_of_listings = dataframe.shape[0]
    count_of_bedrooms = dataframe['bedrooms'].agg('sum')
    fi_stats.append(count_of_listings)
    fi_stats.append(count_of_bedrooms)
    return fi_stats
# basic_stats_df0 = stats(df0)

def updated_stats(datadf, datadfinverse):
    # updated_stats = [] #append like in stats
    count_listings_effected = datadf.shape[0]
    count_listings_not_effected = datadfinverse.shape[0]
    tot_listings = count_listings_effected + count_listings_not_effected
    percentage_effected = round(((count_listings_effected/tot_listings)* 100),2)
    count_bedrooms_effected = datadf['bedrooms'].agg('sum')
    count_bedrooms_uneffected=datadfinverse['bedrooms'].agg('sum')
    tot_bedrooms = count_bedrooms_effected + count_bedrooms_uneffected
    percentage_bed_effected = round(((count_bedrooms_effected/tot_bedrooms) * 100),2)
    return count_listings_effected, count_bedrooms_effected, percentage_effected, percentage_bed_effected


def ltr_stats(datadf):
    # entire units LTR, bedroom count LTR 
    returned_units_entire = datadf.loc[datadf['is_entire']==1].shape[0]
    returned_units_bedrooms = datadf['bedrooms'].agg('sum')
    return returned_units_entire, returned_units_bedrooms


def feetax_stats(datadf, datadfcomm, datadfnocomm):
    #fees 
    feestats = []
    # -non comm fee collection (count based on other cities)
    #could be cool to allow user input for this instead of hardcoded 30 and 60
    yearly_fee_nolisc = (datadfnocomm.shape[0] * 30)
    # -commercial fee collection 
    yearly_fee_nolis_comm = (datadfcomm.shape[0] * 60)
    yearly_fee_tot = yearly_fee_nolisc + yearly_fee_nolis_comm
    #taxes 
    # -tax rev increase normal 21% for all 
    # yearly_revenue_nolisc = datadf['rounded_re'].agg('sum')
    yearly_revenue_nolisc = datadf['rounded_revenue_ltm'].agg('sum')
    yearly_increased_tax_rev_21 = yearly_revenue_nolisc * .21
    # # -tax rev increase normal 30% -tax increase commercial 60% 
    # yearly_rev_nolisc_comm = datadfcomm['rounded_re'].agg('sum')
    # yearly_rev_nolisc_nocomm = datadfnocomm['rounded_re'].agg('sum')
    yearly_rev_nolisc_comm = datadfcomm['rounded_revenue_ltm'].agg('sum')
    yearly_rev_nolisc_nocomm = datadfnocomm['rounded_revenue_ltm'].agg('sum')
    #could be cool to allow user input for this instead of hardcoded 30 and 60
    total_revenue_all_hosts = yearly_rev_nolisc_comm + yearly_rev_nolisc_nocomm
    yearly_rev_comm = (yearly_rev_nolisc_comm * .60)
    yearly_rev_nocomm = (yearly_rev_nolisc_nocomm * .30) 
    yearly_rev_tot = yearly_rev_nocomm + yearly_rev_comm
    feestats.append(round(total_revenue_all_hosts, 2))
    feestats.append(round(yearly_fee_tot,2)) #increased fee permit 
    feestats.append(round(yearly_increased_tax_rev_21,2)) #no liscense at 21% tax lost 
    feestats.append(round(yearly_rev_tot,2)) #no lisc comm and noncomm differentiate tax 30% and 60%
    return feestats

# feestats_list = feetax_stats(policy1_df0, policy1_df0_comm, policy1_df0_nocomm)
def get_stats():
    df = load_database_data() #change this to make less slow
    # df = config.df_database
    df0 = clean_dataframe(df)
    fi_stats = stats(df0)
    return fi_stats

def get_updated_stats():
    list_of_updated_stats = []
    df = load_database_data() #change this to make less slow
    # df = config.df_database
    df0 = clean_dataframe(df) #should not be doing it this way load in config file as global but ok for now
    no_lisc_df0, lisc_df0, comm_no_lisc_df0, nocomm_no_lisc_df0, entire_df0, not_entire_df0, many_listings_df0, not_many_listings_df0 = create_specific_dataframes(df0) 
    pol1_stats = updated_stats(no_lisc_df0,lisc_df0)
    #for no liscense this is count_listings_effected, count_bedrooms_effected, percentage_effected, percentage_bed_effected
    pol2_stats = updated_stats(entire_df0, not_entire_df0)
    #for no entirethis is count_listings_effected, count_bedrooms_effected, percentage_effected, percentage_bed_effected
    pol3_stats = updated_stats(many_listings_df0, not_many_listings_df0)
    #for no many this is count_listings_effected, count_bedrooms_effected, percentage_effected, percentage_bed_effected
    list_of_updated_stats.append(pol1_stats)
    list_of_updated_stats.append(pol2_stats)
    list_of_updated_stats.append(pol3_stats)
    return list_of_updated_stats
#here we can overlay the census choropleth for the orignal map
#this map is for the census assess non airbnb template
def census_map(mapdf, tileinfo, attribinfo):
    census_geo = "/Users/stateofplace/new_codes/geodjango_tut/csv/joined_census_neigh_dj.geojson"
    census_data = "/Users/stateofplace/new_codes/geodjango_tut/csv/num_air_pop_census_dj.csv"
    census_data2 = "/Users/stateofplace/new_codes/geodjango_tut/csv/map1_4_census_by_pop_dj.csv"
    census_df = pd.read_csv(census_data)
    census_df2 = pd.read_csv(census_data2)
    #insert neighbhorhood 
    #map layer four: neighborhood rent burden
    florence_geo = "/Users/stateofplace/new_codes/geodjango_tut/csv/florence_neighbourhoods_dj.geojson"
    florence_data = "/Users/stateofplace/new_codes/geodjango_tut/csv/rent_burden_neigh_dj.csv"
    florence_df = pd.read_csv(florence_data)

    census_map = folium.Map(location=[mapdf.latitude.mean(),mapdf.longitude.mean()], zoom_start=12, control_scale=True, tiles='CartoDB Positron', attr=attribinfo)
    #map layer one: rentership rates
    bins = list(census_df2["a47_by100"].quantile([0, 0.25, 0.5, 0.75, 1]))
    folium.Choropleth(
        geo_data = census_geo,
        # geo_data = geo_census,
        name="Renters per Capita",
        data = census_df2,
        # data=census_df,
        columns=["SEZ2011", "a47_by100"],
        # columns=["SEZ2011", "field_1"],
        key_on= "properties.SEZ2011",
        # key_on="features.geometry.SEZ2011", #in geojson where to find coordinates, a bit of a guess
        fill_color='Pastel2', #find a colorbrewer code
        fill_opacity=0.7,
        line_opacity=0.2,
        bins=bins, #make your own bins
        nan_fill_color='white',
        highlight=True,
        legend_name= "Rate of Renters per 100 residents",   
        reset=True, #not sure what this does 
    ).add_to(census_map)

    bins_4 = list(florence_df["rent_burden"].quantile([0., 0.25, 0.50, 0.75, 1.]))
    folium.Choropleth(
        geo_data = florence_geo,
        # geo_data = geo_census,
        name="Rent Burden Percent",
        data = florence_df,
        # data=census_df,
        columns=["neighbourhood_cleansed", "rent_burden"],
        # columns=["SEZ2011", "field_1"],
        key_on= "feature.properties.neighbourhood",
        # key_on="features.geometry.SEZ2011", #in geojson where to find coordinates, a bit of a guess
        fill_color='Pastel1', #find a colorbrewer code
        fill_opacity=0.7,
        line_opacity=0.2,
        bins=bins_4, #make your own bins
        nan_fill_color='white',
        highlight=True,
        legend_name= "Neighborhood Rent Burden %", 
        reset=True, #not sure what this does 
    ).add_to(census_map)
    folium.CircleMarker(location=[43.7731, 11.2560], radius=2, color="orange", fill=True, fill_color ="orange", fill_opacity= 1, opacity=1, tooltip="Duomo", popup="Duomo").add_to(census_map)


    folium.LayerControl().add_to(census_map)
    # census_map.save('census_map.html')
    return census_map



#this map is for the policy landing page template
def original_airbnb_map(mapdf, tileinfo, attribinfo, filetitle):
    #create bubble map
    bub_map = folium.Map(location=[mapdf.latitude.mean(),mapdf.longitude.mean()], zoom_start=12, control_scale=True, tiles='CartoDB Positron', attr=attribinfo) 

    for index, location_info in mapdf.iterrows():
        #here we declare all variables from model
        host_id = location_info["host_id"]
        host_name = location_info["host_name"]
        license = location_info["license"]
        listing_url = location_info["listing_url"]
        listing_id = location_info["id"]
        listing_name = location_info["name"]
        host_since = location_info["host_since"]
        host_total_listings_count = location_info["host_total_listings_count"]
        host_location =  location_info["host_florence"] #TODO edit with logic
        neighbourhood_cleansed = location_info["neighbourhood_cleansed"]
        dist_duomo = round(location_info["dist_duomo"]) #check if in meters or ft
        room_type = location_info["room_type"]
        bedrooms = location_info["bedrooms"]
        accommodates = location_info["accommodates"]
        rounded_revenue_ltm = round(location_info["rounded_revenue_ltm"], 2)
        monthly_rounded_revenue_ltm = round((rounded_revenue_ltm / 12), 2)
        price = location_info["price"]
        days_rented_ltm = round(location_info["days_rented_ltm"], 2)
        reviews_per_month = location_info["reviews_per_month"]
        #here we create the html text 
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <link href="http://fonts.googleapis.com/css?family=Lato:400,700,900" rel="stylesheet" type="text/css">
        <link href="static/ia_copy_tooltip.css" rel="stylesheet" type="text/css">
        </head>
        <div id="listingHover" class="pinned" style="left: 50px; visibility: visible; top: auto; bottom: 2px;">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="closeHover" style="visibility: visible;"><span aria-hidden="true">×</span></button>
            <div class="hostDetailsContainer">
                <p><a id="listingHost" target="_blank" href="http://www.airbnb.com/users/show/{}">""".format(host_id) + """{}</a>""".format(host_name) + """ ({}) </p>""".format(host_location) + """ 
                <!-- want to say if have liscenese then show the number if not then say no liscnese illegal etc with django template can use if logic block -->
                <p id="listingHostLicense"><span id="listingHostLicense">Hosting since: {}</span>""".format(host_since) + """</p>
                <p id="listingHostLicense"><span id="listingHostLicense">{}</span>""".format(license) + """ No License </p>
                <p id="listingHostCountContainer">(<span id="listingHostListingCount">{}</span>""".format(host_total_listings_count) + """ other listings locally)</p>
            </div>
            <div class="listingDetailsContainer">
                <p id="listingIDContainer"><a id="listingID" target="_blank" href={}>""".format(listing_url) + """ {}</a>""".format(listing_id) + """</p>
                <p id="listingNameContainer"><a id="listingName" target="_blank" href={}>""".format(listing_url) + """{}</a>""".format(listing_name) + """</p>
                <p id="listingNeighbourhood">{}</p>""".format(neighbourhood_cleansed) + """
                <p id="listingNeighbourhoodDistDuomo">{} meters to the Duomo</p>""".format(dist_duomo) + """
                <p id="listingRoomType">{} ({} bedrooms, accommodates {})</p>""".format(room_type, bedrooms, accommodates) + """
            </div>
            <div id="listingPriceSection" class="listingSection">
                <p class="listingSectionHeadlineContainer">
                    <span class="listingSectionHeadline"><span class="dollarSign">€</span><span id="listingEstimatedIncomePerYear">{}</span>""".format(rounded_revenue_ltm) + """</span><span id="listingPriceLabel" class="listingSectionHeadlineLabel"> income/year (est.)</span>
                </p>
                <p <span class="listingSectionSubhead"><span class="dollarSign">€</span><span id="listingEstimatedIncomePerMonth">{}</span>""".format(monthly_rounded_revenue_ltm) + """</span><span id="listingPriceLabel" class="listingSectionSubhead"> income/month (est.)</span> </p>
                <p class="listingSectionSubhead"><span class="dollarSign">€</span><span id="listingPrice">{}</span>""".format(price) + """/night</p>
            </div>
            <div id="listingReviewsSection" class="listingSection">
                <p class="listingSectionHeadlineContainer">
                    <span class="listingSectionSubhead"><span id="listingEstimatedNightsPerYear" class="listingSectionHeadline">{}</span>""".format(days_rented_ltm) + """<span class="listingSectionHeadlineLabel"> nights/year (est.)</span></span>
                </p>
                <!-- <p class="listingSectionSubhead"><span id="listingEstimatedOccupancyRate">23.4</span>% occupancy rate (est.)</p> -->
                <p class="listingSectionSubhead"><span id="listingReviewPerMonth">{}</span>""".format(reviews_per_month) + """ reviews/month</p>
                <!-- <p class="listingSectionSubhead"><span id="listingNumberOfReviews">5</span><span id="listingReviewsLabel"> reviews</span></p> -->
                <!-- <p class="listingSectionSubhead">last: <span id="listingLastReview">31/10/2021</span></p> -->
            </div>
            <div id="listingCensusSection" class= "listingSection">
            </div>
            <p class="listingSection">click listing on map to "pin" details</p>
            <p class="listingSection">the style for this popup was created by <a href="http://insideairbnb.com/">Inside Airbnb</a></p>

        </div>
        </html>
            """  
        folium.CircleMarker([location_info["latitude"],location_info["longitude"]], radius=2, color="blue", fill_opacity= 0.5, opacity=0.5, fill=True, fill_color ="blue", popup=html, tooltip=html).add_to(bub_map)
        # print(location_info["host_id"])

    census_geo = "/Users/stateofplace/new_codes/geodjango_tut/csv/joined_census_neigh_dj.geojson"
    census_data = "/Users/stateofplace/new_codes/geodjango_tut/csv/num_air_pop_census_dj.csv"
    census_df = pd.read_csv(census_data)

    bins_2 = list(census_df["cont_per_1000"].quantile([0, 0.25, 0.5, 0.75, 1]))

    folium.Choropleth(
        geo_data = census_geo,
        # geo_data = geo_census,
        name="Airbnbs Per Capita",
        data = census_df,
        # data=census_df,
        columns=["census_tract_id", "cont_per_1000"],
        # columns=["SEZ2011", "field_1"],
        key_on= "properties.SEZ2011",
        # key_on="features.geometry.SEZ2011", #in geojson where to find coordinates, a bit of a guess
        fill_color='YlGnBu', #find a colorbrewer code
        fill_opacity=0.7,
        line_opacity=0.2,
        bins=bins_2, #make your own bins
        nan_fill_color='white',
        highlight=True,
        legend_name= "Airbnb Listings per 1000 residents",   
        reset=True, #not sure what this does 
    ).add_to(bub_map)

    #map layer three: airbnb per units
    bins_3 = list(census_df["air_e27_per1000"].quantile([0, 0.25, 0.5, 0.75, 1]))
    # m = folium.Map(location=[43.769, 11.255],zoom_start=13, tiles='CartoDB Positron')

    folium.Choropleth(
        geo_data = census_geo,
        # geo_data = geo_census,
        name="Airbnbs Per Units",
        data = census_df,
        # data=census_df,
        columns=["census_tract_id", "air_e27_per1000"],
        # columns=["SEZ2011", "field_1"],
        key_on= "properties.SEZ2011",
        # key_on="features.geometry.SEZ2011", #in geojson where to find coordinates, a bit of a guess
        fill_color='YlGnBu', #find a colorbrewer code
        fill_opacity=0.7,
        line_opacity=0.2,
        bins=bins_3, #make your own bins
        nan_fill_color='white',
        highlight=True,
        legend_name= "Airbnb Listings Per 1000 housing units",   
        reset=True, #not sure what this does 
    ).add_to(bub_map)

    folium.CircleMarker(location=[43.7731, 11.2560], radius=2, color="orange", fill=True, fill_color ="orange", fill_opacity= 1, opacity=1, tooltip="Duomo", popup="Duomo").add_to(bub_map)

    folium.LayerControl().add_to(bub_map)
    # bub_map.save(data_path + '/Out_Map/' + filetitle + '.html')
    return bub_map
#original_airbnb_map(mapdf, datadf, tileinfo)
# original_airbnb_map(df0, esri, attrib, 'original_airbnb_map')

#here we want to switch to red and green dots or yellow on top of blue, and make a legend
#this map is for policyone map template
def updated_airbnb_map(mapdf, datadf, inverse_datadf, tileinfo, attribinfo, filetitle):
    #create updated bubble map after clicking certain policy x
    updated_bub_map = folium.Map(location=[mapdf.latitude.mean(),mapdf.longitude.mean()], zoom_start=12, control_scale=True, tiles='CartoDB Positron', attr=attribinfo) 
    
    #testing why index is grayed out and why yellow doesn't show in my maps... opacity? 
    
    for index, location_info in datadf.iterrows():
        #here we declare all variables from model
        host_id = location_info["host_id"]
        host_name = location_info["host_name"]
        license = location_info["license"]
        listing_url = location_info["listing_url"]
        listing_id = location_info["id"]
        listing_name = location_info["name"]
        host_since = location_info["host_since"]
        host_total_listings_count = location_info["host_total_listings_count"] 
        host_location =  location_info["host_florence"] #TODO edit with logic
        neighbourhood_cleansed = location_info["neighbourhood_cleansed"]
        dist_duomo = round(location_info["dist_duomo"]) #check if in meters or ft
        room_type = location_info["room_type"]
        bedrooms = location_info["bedrooms"]
        accommodates = location_info["accommodates"]
        rounded_revenue_ltm = round(location_info["rounded_revenue_ltm"], 2)
        monthly_rounded_revenue_ltm = round((rounded_revenue_ltm / 12), 2)
        price = location_info["price"]
        days_rented_ltm = round(location_info["days_rented_ltm"], 2)
        reviews_per_month = location_info["reviews_per_month"]
        #here we create the html text 
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <link href="http://fonts.googleapis.com/css?family=Lato:400,700,900" rel="stylesheet" type="text/css">
        <link href="static/ia_copy_tooltip.css" rel="stylesheet" type="text/css">
        </head>
        <div id="listingHover" class="pinned" style="left: 50px; visibility: visible; top: auto; bottom: 2px;">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="closeHover" style="visibility: visible;"><span aria-hidden="true">×</span></button>
            <div class="hostDetailsContainer">
                <p><a id="listingHost" target="_blank" href="http://www.airbnb.com/users/show/{}">""".format(host_id) + """{}</a>""".format(host_name) + """ ({}) </p>""".format(host_location) + """ 
                <!-- want to say if have liscenese then show the number if not then say no liscnese illegal etc with django template can use if logic block -->
                <p id="listingHostLicense"><span id="listingHostLicense">Hosting since: {}</span>""".format(host_since) + """</p>
                <p id="listingHostLicense"><span id="listingHostLicense">{}</span>""".format(license) + """ No License </p>
                <p id="listingHostCountContainer">(<span id="listingHostListingCount">{}</span>""".format(host_total_listings_count) + """ other listings locally)</p>
            </div>
            <div class="listingDetailsContainer">
                <p id="listingIDContainer"><a id="listingID" target="_blank" href={}>""".format(listing_url) + """ {}</a>""".format(listing_id) + """</p>
                <p id="listingNameContainer"><a id="listingName" target="_blank" href={}>""".format(listing_url) + """{}</a>""".format(listing_name) + """</p>
                <p id="listingNeighbourhood">{}</p>""".format(neighbourhood_cleansed) + """
                <p id="listingNeighbourhoodDistDuomo">{} meters to the Duomo</p>""".format(dist_duomo) + """
                <p id="listingRoomType">{} ({} bedrooms, accommodates {})</p>""".format(room_type, bedrooms, accommodates) + """
            </div>
            <div id="listingPriceSection" class="listingSection">
                <p class="listingSectionHeadlineContainer">
                    <span class="listingSectionHeadline"><span class="dollarSign">€</span><span id="listingEstimatedIncomePerYear">{}</span>""".format(rounded_revenue_ltm) + """</span><span id="listingPriceLabel" class="listingSectionHeadlineLabel"> income/year (est.)</span>
                </p>
                <p <span class="listingSectionSubhead"><span class="dollarSign">€</span><span id="listingEstimatedIncomePerMonth">{}</span>""".format(monthly_rounded_revenue_ltm) + """</span><span id="listingPriceLabel" class="listingSectionSubhead"> income/month (est.)</span> </p>
                <p class="listingSectionSubhead"><span class="dollarSign">€</span><span id="listingPrice">{}</span>""".format(price) + """/night</p>
            </div>
            <div id="listingReviewsSection" class="listingSection">
                <p class="listingSectionHeadlineContainer">
                    <span class="listingSectionSubhead"><span id="listingEstimatedNightsPerYear" class="listingSectionHeadline">{}</span>""".format(days_rented_ltm) + """<span class="listingSectionHeadlineLabel"> nights/year (est.)</span></span>
                </p>
                <!-- <p class="listingSectionSubhead"><span id="listingEstimatedOccupancyRate">23.4</span>% occupancy rate (est.)</p> -->
                <p class="listingSectionSubhead"><span id="listingReviewPerMonth">{}</span>""".format(reviews_per_month) + """ reviews/month</p>
                <!-- <p class="listingSectionSubhead"><span id="listingNumberOfReviews">5</span><span id="listingReviewsLabel"> reviews</span></p> -->
                <!-- <p class="listingSectionSubhead">last: <span id="listingLastReview">31/10/2021</span></p> -->
            </div>
            <div id="listingCensusSection" class= "listingSection">
            </div>
            <p class="listingSection">click listing on map to "pin" details</p>
            <p class="listingSection">the style for this popup was created by <a href="http://insideairbnb.com/">Inside Airbnb</a></p>
        </div>
        </html>
            """  
        folium.CircleMarker([location_info["latitude"],location_info["longitude"]], radius=2, color="grey", fill=True, fill_color ="grey", fill_opacity= 0.5, opacity=0.5, popup=html, tooltip=html).add_to(updated_bub_map)
    for index, location_info in inverse_datadf.iterrows():
         #here we declare all variables from model
        host_id = location_info["host_id"]
        host_name = location_info["host_name"]
        license = location_info["license"]
        listing_url = location_info["listing_url"]
        listing_id = location_info["id"]
        listing_name = location_info["name"]
        host_since = location_info["host_since"]
        host_total_listings_count = location_info["host_total_listings_count"] 
        host_location =  location_info["host_florence"] #TODO edit with logic
        neighbourhood_cleansed = location_info["neighbourhood_cleansed"]
        dist_duomo = round(location_info["dist_duomo"]) #check if in meters or ft
        room_type = location_info["room_type"]
        bedrooms = location_info["bedrooms"]
        accommodates = location_info["accommodates"]
        rounded_revenue_ltm = round(location_info["rounded_revenue_ltm"], 2)
        monthly_rounded_revenue_ltm = round((rounded_revenue_ltm / 12), 2)
        price = location_info["price"]
        days_rented_ltm = round(location_info["days_rented_ltm"], 2)
        reviews_per_month = location_info["reviews_per_month"]
        #here we create the html text 
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <link href="http://fonts.googleapis.com/css?family=Lato:400,700,900" rel="stylesheet" type="text/css">
        <link href="static/ia_copy_tooltip.css" rel="stylesheet" type="text/css">
        </head>
        <div id="listingHover" class="pinned" style="left: 50px; visibility: visible; top: auto; bottom: 2px;">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="closeHover" style="visibility: visible;"><span aria-hidden="true">×</span></button>
            <div class="hostDetailsContainer">
                <p><a id="listingHost" target="_blank" href="http://www.airbnb.com/users/show/{}">""".format(host_id) + """{}</a>""".format(host_name) + """ ({}) </p>""".format(host_location) + """ 
                <!-- want to say if have liscenese then show the number if not then say no liscnese illegal etc with django template can use if logic block -->
                <p id="listingHostLicense"><span id="listingHostLicense">Hosting since: {}</span>""".format(host_since) + """</p>
                <p id="listingHostLicense"><span id="listingHostLicense">{}</span>""".format(license) + """ No License </p>
                <p id="listingHostCountContainer">(<span id="listingHostListingCount">{}</span>""".format(host_total_listings_count) + """ other listings locally)</p>
            </div>
            <div class="listingDetailsContainer">
                <p id="listingIDContainer"><a id="listingID" target="_blank" href={}>""".format(listing_url) + """ {}</a>""".format(listing_id) + """</p>
                <p id="listingNameContainer"><a id="listingName" target="_blank" href={}>""".format(listing_url) + """{}</a>""".format(listing_name) + """</p>
                <p id="listingNeighbourhood">{}</p>""".format(neighbourhood_cleansed) + """
                <p id="listingNeighbourhoodDistDuomo">{} meters to the Duomo</p>""".format(dist_duomo) + """
                <p id="listingRoomType">{} ({} bedrooms, accommodates {})</p>""".format(room_type, bedrooms, accommodates) + """
            </div>
            <div id="listingPriceSection" class="listingSection">
                <p class="listingSectionHeadlineContainer">
                    <span class="listingSectionHeadline"><span class="dollarSign">€</span><span id="listingEstimatedIncomePerYear">{}</span>""".format(rounded_revenue_ltm) + """</span><span id="listingPriceLabel" class="listingSectionHeadlineLabel"> income/year (est.)</span>
                </p>
                <p <span class="listingSectionSubhead"><span class="dollarSign">€</span><span id="listingEstimatedIncomePerMonth">{}</span>""".format(monthly_rounded_revenue_ltm) + """</span><span id="listingPriceLabel" class="listingSectionSubhead"> income/month (est.)</span> </p>
                <p class="listingSectionSubhead"><span class="dollarSign">€</span><span id="listingPrice">{}</span>""".format(price) + """/night</p>
            </div>
            <div id="listingReviewsSection" class="listingSection">
                <p class="listingSectionHeadlineContainer">
                    <span class="listingSectionSubhead"><span id="listingEstimatedNightsPerYear" class="listingSectionHeadline">{}</span>""".format(days_rented_ltm) + """<span class="listingSectionHeadlineLabel"> nights/year (est.)</span></span>
                </p>
                <!-- <p class="listingSectionSubhead"><span id="listingEstimatedOccupancyRate">23.4</span>% occupancy rate (est.)</p> -->
                <p class="listingSectionSubhead"><span id="listingReviewPerMonth">{}</span>""".format(reviews_per_month) + """ reviews/month</p>
                <!-- <p class="listingSectionSubhead"><span id="listingNumberOfReviews">5</span><span id="listingReviewsLabel"> reviews</span></p> -->
                <!-- <p class="listingSectionSubhead">last: <span id="listingLastReview">31/10/2021</span></p> -->
            </div>
            <div id="listingCensusSection" class= "listingSection">
            </div>
            <p class="listingSection">click listing on map to "pin" details</p>
        </div>
        </html>
            """  
        folium.CircleMarker([location_info["latitude"],location_info["longitude"]], radius=2, color="blue", fill=True, fill_color ="blue", fill_opacity= 0.2, opacity=0.2, popup=html, tooltip=html).add_to(updated_bub_map)
    folium.LayerControl().add_to(updated_bub_map)
    folium.CircleMarker(location=[43.7731, 11.2560], radius=2, color="orange", fill=True, fill_color ="orange", fill_opacity= 1, opacity=1, tooltip="Duomo", popup="Duomo").add_to(updated_bub_map)

    # updated_bub_map.save(data_path + '/Out_Map/' + filetitle + '.html')

    return updated_bub_map
# updated_airbnb_map(df0, policy1_df0, policy1_df0_inverse, esri, attrib, 'policy4_df0_funct')

def get_orig_map():
    # df = load_csv_data(data_path + '/csv_ia/test_file.csv') #/Users/stateofplace/new_codes/geodjango_tut/geodjango/world/test_file.csv
    df = load_database_data() 
    #df = config.df_database
    df0 = clean_dataframe(df)
    orig_map = original_airbnb_map(df0, esri, attrib, 'original_airbnb_map_script')
    return orig_map


#trying to insert df0 instead of calling it in the function... why was I calling it in here?
#doesn't work, but maybe instead of calling this function in views we can just pass the result?
def getbubmaps():
    # df = load_csv_data(data_path + '/csv_ia/test_file.csv') #/Users/stateofplace/new_codes/geodjango_tut/geodjango/world/test_file.csv
    df = load_database_data() 
    # df = config.df_database
    df0 = clean_dataframe(df)
    policy1_df0, policy1_df0_inverse, policy1_df0_comm, policy1_df0_nocomm, policy2_df0, policy2_df0_inverse, policy3_df0, policy3_df0_inverse = create_specific_dataframes(df0)
    # basic_stats_df0 = stats(df0)
    # feestats_list = feetax_stats(policy1_df0, policy1_df0_comm, policy1_df0_nocomm)

    bubmap = original_airbnb_map(df0, esri, attrib, 'original_airbnb_map_script')
    updatedbubmap_1 = updated_airbnb_map(df0, policy1_df0, policy1_df0_inverse, esri, attrib, 'policy1_df0_funct_script')
    updatedbubmap_2 = updated_airbnb_map(df0, policy2_df0, policy2_df0_inverse, esri, attrib, 'policy2_df0_funct_script')
    updatedbubmap_3 = updated_airbnb_map(df0, policy3_df0, policy3_df0_inverse, esri, attrib, 'policy3_df0_funct_script')
    #census map referenced befor assignement i don't get it i'm doing the same for bubmap and the rest 
    census_choro_map = census_map(df0, esri, attrib)
    # updated_stats = updated_stats(policy1_df0, policy1_df0_inverse) 
    # ltr_stats = ltr_stats(policy1_df0) 
    #MUST RETURN THINGS!!!! 
    #here we can return all the maps for all the policies etc, then in views call them by the [0]
    # bubmap = original_airbnb_map(df0, esri, attrib, 'original_airbnb_map_script')
    return bubmap, updatedbubmap_1, updatedbubmap_2, updatedbubmap_3, census_choro_map

def popup_html(row):
    # html ="hello"  #this worked, we can do this. niente
    # html = row #this also worked, we can do this! i
    # html = row_price #this ALSO worked, we can def do this!! i.price
    
    #here we declare all variables from model
    host_id = row.host_id #dummy id #should work... row.host_id
    host_name = row.host_name
    host_since = row.host_since
    host_location = row.host_location
    license = row.license
    host_total_listings_count = row.host_total_listings_count
    # global_total_listings = row.global_total_listings
    listing_url = row.listing_url
    listing_id = row.id
    listing_name = row.name
    neighbourhood_cleansed = row.neighbourhood_cleansed
    dist_duomo = round(row.dist_duomo) #check if in meters or ft
    room_type = row.room_type
    bedrooms = row.bedrooms
    accommodates = row.accommodates
    rounded_revenue_ltm = round(row.rounded_revenue_ltm, 2)
    monthly_rounded_revenue_ltm = round((rounded_revenue_ltm / 12), 2)
    price = row.price
    night_min = 2 #dummy placeholder
    days_rented_ltm = round(row.days_rented_ltm, 2)
    reviews_per_month = row.reviews_per_month
    # census_tract = 8972720.3 #dummy placeholder
    # number_listings_census = 40 #dummy placeholder
    # number_elderly_census = 20 #dummy placeholder 
    # number_single_parent_census = 10 #dummy placeholder 
    # rent_burden_census = "HIGH" #low, medium, high
    # census_homeowners = 33 #dummy placeholder

    #here we create the html text 
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <link href="http://fonts.googleapis.com/css?family=Lato:400,700,900" rel="stylesheet" type="text/css">
    <link href="static/ia_copy_tooltip.css" rel="stylesheet" type="text/css">
    </head>
    <div id="listingHover" class="pinned" style="left: 50px; visibility: visible; top: auto; bottom: 2px;">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="closeHover" style="visibility: visible;"><span aria-hidden="true">×</span></button>
        <div class="hostDetailsContainer">
            <p><a id="listingHost" target="_blank" href="http://www.airbnb.com/users/show/{}">""".format(host_id) + """{}</a>""".format(host_name) + """ ({}) </p>""".format(host_location) + """ 
            <!-- want to say if have liscenese then show the number if not then say no liscnese illegal etc with django template can use if logic block -->
            <p id="listingHostLicense"><span id="listingHostLicense">Hosting since: {}</span>""".format(host_since) + """</p>
            <p id="listingHostLicense"><span id="listingHostLicense">{}</span>""".format(license) + """ No License </p>
            <p id="listingHostCountContainer">(<span id="listingHostListingCount">{}</span>""".format(host_total_listings_count) + """ other listings locally)</p>
        </div>
        <div class="listingDetailsContainer">
            <p id="listingIDContainer"><a id="listingID" target="_blank" href={}>""".format(listing_url) + """ {}</a>""".format(listing_id) + """</p>
            <p id="listingNameContainer"><a id="listingName" target="_blank" href={}>""".format(listing_url) + """{}</a>""".format(listing_name) + """</p>
            <p id="listingNeighbourhood">{}</p>""".format(neighbourhood_cleansed) + """
            <p id="listingNeighbourhoodDistDuomo">{} meters to the Duomo</p>""".format(dist_duomo) + """
            <p id="listingRoomType">{} ({} bedrooms, accommodates {})</p>""".format(room_type, bedrooms, accommodates) + """
        </div>
        <div id="listingPriceSection" class="listingSection">
            <p class="listingSectionHeadlineContainer">
                <span class="listingSectionHeadline"><span class="dollarSign">€</span><span id="listingEstimatedIncomePerYear">{}</span>""".format(rounded_revenue_ltm) + """</span><span id="listingPriceLabel" class="listingSectionHeadlineLabel"> income/year (est.)</span>
            </p>
            <p <span class="listingSectionSubhead"><span class="dollarSign">€</span><span id="listingEstimatedIncomePerMonth">{}</span>""".format(monthly_rounded_revenue_ltm) + """</span><span id="listingPriceLabel" class="listingSectionSubhead"> income/month (est.)</span> </p>
            <p class="listingSectionSubhead"><span class="dollarSign">€</span><span id="listingPrice">{}</span>""".format(price) + """/night</p>
            <p class="listingSectionSubhead"><span id="listingMinimumNights">{}</span>""".format(night_min) + """ night minimum</p>
        </div>
        <div id="listingReviewsSection" class="listingSection">
            <p class="listingSectionHeadlineContainer">
                <span class="listingSectionSubhead"><span id="listingEstimatedNightsPerYear" class="listingSectionHeadline">{}</span>""".format(days_rented_ltm) + """<span class="listingSectionHeadlineLabel"> nights/year (est.)</span></span>
            </p>
            <!-- <p class="listingSectionSubhead"><span id="listingEstimatedOccupancyRate">23.4</span>% occupancy rate (est.)</p> -->
            <p class="listingSectionSubhead"><span id="listingReviewPerMonth">{}</span>""".format(reviews_per_month) + """ reviews/month</p>
            <!-- <p class="listingSectionSubhead"><span id="listingNumberOfReviews">5</span><span id="listingReviewsLabel"> reviews</span></p> -->
            <!-- <p class="listingSectionSubhead">last: <span id="listingLastReview">31/10/2021</span></p> -->
        </div>
        <div id="listingCensusSection" class= "listingSection">
        </div>
        <p class="listingSection">click listing on map to "pin" details</p>
    </div>
    </html>
        """  
    return html


#only need if running this as a script not importing
#tried this to maybe speed things up, so far made poliyc1 longer, 2min to 2.4min, but maybe it'll help others?
# def main():
#     pass
# if __name__ == '__main__':
#     main()
#     census_map()
#     # load_database_data()
#     get_orig_map()
#     # getbubmaps()
    


