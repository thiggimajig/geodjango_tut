import geojson
# import geopandas
import pandas as pd
import numpy as np
import statistics as st
import matplotlib as plt
import folium
from folium.features import CustomIcon
import csv
from IPython.display import display, HTML
from pathlib import Path 
import os
import sys
from .models import AirbnbListings 
# from models import AirbnbListings 
data_path = os.path.abspath('/Users/stateofplace/new_codes/geodjango_tut/geodjango/world/data/')
sys.path.append(data_path)
# sys.path.append("/geodjango/world/data/policy_functions")
#example of absolute path settting for file... 
# dirpath = os.path.dirname(os.path.abspath(__file__))
# chap_dirpath = os.path.join(dirpath, chap_dirpath)


esri = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
attrib = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'

#TODO FOR REFACTOR: i think i need to atleast change the first two functions so that the data comes from the database not a csv file 
#found this from ... https://stackoverflow.com/questions/11697887/converting-django-queryset-to-pandas-dataframe 
#an alternative method # Convert Django's Queryset into a Pandas DataFrame: pricing_dataframe = pd.DataFrame.from_records(prices.values())

def load_database_data():
    df = pd.DataFrame(list(AirbnbListings.objects.all().values('id', 'has_liscense', 'days_rented_ltm', 'rounded_revenue_ltm', 'price', 'name', 'host_id', 'bedrooms', 'many_listings', 'availability_365', 'is_hotel', 'host_name', 'commercial', 'is_entire', 'latitude', 'longitude')))
    print(df.head())
    return df
df = load_database_data()
#load up csv file into df
#here we are loading the data from a csv file... but we can just as easily do that from the model
# def load_csv_data(ia):
#     ia_df = pd.read_csv(ia)
#     return ia_df
# # df = load_csv_data(data_path + 'csv_ia/test_file.csv')

#here we create the cleaned dataframe we want having dropped things we don't care about...but that'll change
def clean_dataframe(s):
    columns_df0 = ['id', 'has_liscense', 'days_rented_ltm', 'rounded_revenue_ltm', 'price', 'name', 'host_id', 'bedrooms', 'many_listings', 'availability_365', 'is_hotel', 'host_name', 'commercial', 'is_entire', 'latitude', 'longitude']
    cleaned_df = s.loc[:,columns_df0]
    return cleaned_df
df0 = clean_dataframe(df)


#here from that cleaned data frame i make dataframes with data specific for each policy function...
#but i can instead make the dataframes with specific data by looping through the model database data
def create_specific_dataframes(s):
    #policy1 df
    no_lisc_df0 = (s.loc[s['has_liscense'] == 0])
    lisc_df0 = (s.loc[s['has_liscense'] == 1])
    #policy1 comm df
    comm_no_lisc_df0 = (no_lisc_df0.loc[no_lisc_df0['commercial'] == 1])
    nocomm_no_lisc_df0 = (no_lisc_df0.loc[no_lisc_df0['commercial'] == 0])
    #policy2 df
    entire_df0 = (s.loc[s['is_entire'] == 1])
    not_entire_df0 = (s.loc[s['is_entire'] == 0])
    #policy3 df
    many_listings_df0 = (s.loc[s['many_listings'] == 1])
    not_many_listings_df0 = (s.loc[s['many_listings'] == 0])

    return no_lisc_df0, lisc_df0, comm_no_lisc_df0, nocomm_no_lisc_df0, entire_df0, not_entire_df0, many_listings_df0, not_many_listings_df0

policy1_df0, policy1_df0_inverse, policy1_df0_comm, policy1_df0_nocomm, policy2_df0, policy2_df0_inverse, policy3_df0, policy3_df0_inverse = create_specific_dataframes(df0)

#here i create basic stats from the entire data...but if i can loop through all rows in the model i can accomplish this or I can use the new dataframes with the model data if we go that route
def stats(dataframe):
    #calculate stats for given area before any regulation
    fi_stats = []
    count_of_listings = dataframe.shape[0]
    count_of_bedrooms = dataframe['bedrooms'].agg('sum')
    fi_stats.append(count_of_listings)
    fi_stats.append(count_of_bedrooms)
    return fi_stats
basic_stats_df0 = stats(df0)

def updated_stats(datadf, datadfinverse):
    count_listings_effected = datadf.shape[0]
    count_listings_not_effected = datadfinverse.shape[0]
    return count_listings_effected, count_listings_not_effected


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
    yearly_rev_nocomm = (yearly_rev_nolisc_nocomm * .30) 
    yearly_rev_comm = (yearly_rev_nolisc_comm * .60)
    yearly_rev_tot = yearly_rev_nocomm + yearly_rev_comm
    feestats.append(round(yearly_fee_tot,2))
    feestats.append(round(yearly_increased_tax_rev_21,2))
    feestats.append(round(yearly_rev_tot,2))
    return feestats

feestats_list = feetax_stats(policy1_df0, policy1_df0_comm, policy1_df0_nocomm)


#here we can overlay the census choropleth for the orignal map
def original_airbnb_map(mapdf, tileinfo, attribinfo, filetitle):
    #create bubble map
    bub_map = folium.Map(location=[mapdf.latitude.mean(),mapdf.longitude.mean()], zoom_start=12, control_scale=True, tiles=tileinfo, attr=attribinfo) 
    folium.LayerControl().add_to(bub_map)
    # TODO change 1 to yes and had total listings and if in florence and make more maps for commercial and not in florence 
    for index, location_info in mapdf.iterrows():
        folium.CircleMarker([location_info["latitude"],location_info["longitude"]], radius=2, color="black", fill=True, fill_color ="black",  popup="name: <br>" + str((location_info["name"])) + " hostname: <br> " + str(location_info["host_name"]) + " Commercial Property : <br> " + str(location_info["commercial"]) + " Price: <br>" + str(location_info["price"]), tooltip="yearly revenue: " + str(location_info["rounded_revenue_ltm"])).add_to(bub_map)
    bub_map.save(data_path + '/Out_Map/' + filetitle + '.html')
    return bub_map
#original_airbnb_map(mapdf, datadf, tileinfo)
original_airbnb_map(df0, esri, attrib, 'original_airbnb_map')


#here we want to switch to red and green dots or yellow on top of blue, and make a legend
def updated_airbnb_map(mapdf, datadf, inverse_datadf, tileinfo, attribinfo, filetitle):
    #create updated bubble map after clicking certain policy x
    updated_bub_map = folium.Map(location=[mapdf.latitude.mean(),mapdf.longitude.mean()], zoom_start=12, control_scale=True, tiles=tileinfo, attr=attribinfo) 
    folium.LayerControl().add_to(updated_bub_map)
    for index, location_info in datadf.iterrows():
        folium.CircleMarker([location_info["latitude"],location_info["longitude"]], radius=2, color="crimson", fill=True, fill_color ="crimson",  popup="name: <br>" + str((location_info["name"])) + " hostname: <br> " + str(location_info["host_name"]) + " Commercial Property : <br> " + str(location_info["commercial"]) + " Price: <br>" + str(location_info["price"]), tooltip="yearly revenue: " + str(location_info["rounded_revenue_ltm"])).add_to(updated_bub_map)
    
    for index, location_info in inverse_datadf.iterrows():
        folium.CircleMarker([location_info["latitude"],location_info["longitude"]], radius=2, color="blue", fill=True, fill_color ="blue",  popup="name: <br>" + str((location_info["name"])) + " hostname: <br> " + str(location_info["host_name"]) + " Commercial Property : <br> " + str(location_info["commercial"]) + " Price: <br>" + str(location_info["price"]), tooltip="yearly revenue: " + str(location_info["rounded_revenue_ltm"])).add_to(updated_bub_map)
    updated_bub_map.save(data_path + '/Out_Map/' + filetitle + '.html')

    return updated_bub_map
updated_airbnb_map(df0, policy1_df0, policy1_df0_inverse, esri, attrib, 'policy4_df0_funct')

def get_orig_map():
    # df = load_csv_data(data_path + '/csv_ia/test_file.csv') #/Users/stateofplace/new_codes/geodjango_tut/geodjango/world/test_file.csv
    df = load_database_data() 
    df0 = clean_dataframe(df)
    bubmap = original_airbnb_map(df0, esri, attrib, 'original_airbnb_map_script')
    return bubmap
  

def getbubmaps():
    # df = load_csv_data(data_path + '/csv_ia/test_file.csv') #/Users/stateofplace/new_codes/geodjango_tut/geodjango/world/test_file.csv
    df = load_database_data() 
    df0 = clean_dataframe(df)
    policy1_df0, policy1_df0_inverse, policy1_df0_comm, policy1_df0_nocomm, policy2_df0, policy2_df0_inverse, policy3_df0, policy3_df0_inverse, = create_specific_dataframes(df0)
    # basic_stats_df0 = stats(df0)
    # feestats_list = feetax_stats(policy1_df0, policy1_df0_comm, policy1_df0_nocomm)
    bubmap = original_airbnb_map(df0, esri, attrib, 'original_airbnb_map_script')
    updatedbubmap_1 = updated_airbnb_map(df0, policy1_df0, policy1_df0_inverse, esri, attrib, 'policy1_df0_funct_script')
    updatedbubmap_2 = updated_airbnb_map(df0, policy2_df0, policy2_df0_inverse, esri, attrib, 'policy2_df0_funct_script')
    updatedbubmap_3 = updated_airbnb_map(df0, policy3_df0, policy3_df0_inverse, esri, attrib, 'policy3_df0_funct_script')
    # updated_stats = updated_stats(policy1_df0, policy1_df0_inverse) 
    # ltr_stats = ltr_stats(policy1_df0) 
    #MUST RETURN THINGS!!!! 
    #here we can return all the maps for all the policies etc, then in views call them by the [0]
    bubmap = original_airbnb_map(df0, esri, attrib, 'original_airbnb_map_script')
    return bubmap, updatedbubmap_1, updatedbubmap_2, updatedbubmap_3

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
    census_tract = 8972720.3 #dummy placeholder
    number_listings_census = 40 #dummy placeholder
    number_elderly_census = 20 #dummy placeholder 
    number_single_parent_census = 10 #dummy placeholder 
    rent_burden_census = "HIGH" #low, medium, high
    census_homeowners = 33 #dummy placeholder

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
    <p class="listingSeciotnHeadlineContainer">
        <span id="listingCensusInfo" class="listingSectionHeadline">{}</span>""".format(rent_burden_census) + """<span class="listingSectionHeadlineLabel"> rent burden</span>
    </p>
    <p class="listingSectionSubhead"><span id="listingCensusId">Census Tract ID: {}</span>""".format(census_tract) + """</p>
    <p class="listingSectionSubhead"><span id="listingHomeowner"> {}% of neighbors rent""".format(census_homeowners) + """% of block rents </span></p>
    <p class="listingSectionSubhead"><span id="listingCensusNumberListing"> {}""".format(number_listings_census) + """% of block is on airbnb</span></p>
    <p class="listingSectionSubhead"><span id="listingElderly"> {}""".format(number_elderly_census) + """% of neighbors are elderly</span></p>
    <p class="listingSectionSubhead"><span id="listingParent"> {}""".format(number_single_parent_census) + """% of neighbors are single parent</span></p>

    </div>
    <!-- <div id="listingAvailabilitySection" class="listingSection">
        <p class="listingSectionHeadlineContainer">
            <span id="listingAvailabilityDescription" class="listingSectionHeadline">LOW</span><span class="listingSectionHeadlineLabel"> availability</span>
        </p>
        <p class="listingSectionSubhead"><span id="listingAvailability365">0</span> days/year (<span id="listingAvailabilityPercentage">0</span>%)</p>
    </div> -->
    <p class="listingSection">click listing on map to "pin" details</p>
</div>
</html>
    """  
    return html
#only need if running this as a script not importing
# def main():
# if __name__ == '__main__':
#     main()


