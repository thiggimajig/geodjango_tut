import geojson
import geopandas
import pandas as pd
import numpy as np
import statistics as st
import matplotlib as plt
import folium
from folium.features import CustomIcon
import csv
from IPython.display import display, HTML
from pathlib import Path 

#load up csv file into df
def load_csv_data(ia):
    ia_df = pd.read_csv(ia)
    return ia_df
# df = load_csv_data('../thesis_app/Out_CSV/ia_1_27_222022_03_23_18_40_54_new_variables.csv')

def clean_dataframe(s):
    columns_df0 = ['id', 'has_liscense', 'days_rented', 'rounded_revenue', 'price', 'name', 'host_id', 'bedrooms', 'many_listings', 'availability_365', 'is_hotel', 'host_name', 'commercial', 'is_entire', 'latitude', 'longitude']
    cleaned_df = s.loc[:,columns_df0]
    return cleaned_df
# df0 = clean_dataframe(df)

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
    #policy4 df #needs to be better, not just available, has to also be frequently used... but to get frequently used have to see if new or old, new use last month, old use last year pre and post covid 
    cap_days_df0 = (s.loc[s['availability_365'] > 90])
    not_cap_days_df0 = (s.loc[s['availability_365'] < 90])
    return no_lisc_df0, lisc_df0, comm_no_lisc_df0, nocomm_no_lisc_df0, entire_df0, not_entire_df0, many_listings_df0, not_many_listings_df0, cap_days_df0, not_cap_days_df0

# policy1_df0, policy1_df0_inverse, policy1_df0_comm, policy1_df0_nocomm, policy2_df0, policy2_df0_inverse, policy3_df0, policy3_df0_inverse, policy4_df0, policy4_df0_inverse = create_specific_dataframes(df0)

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
    yearly_fee_nolisc = (datadfnocomm.shape[0] * 30)
    # -commercial fee collection 
    yearly_fee_nolis_comm = (datadfcomm.shape[0] * 60)
    yearly_fee_tot = yearly_fee_nolisc + yearly_fee_nolis_comm
    #taxes 
    # -tax rev increase normal 21% for all 
    # yearly_revenue_nolisc = datadf['rounded_re'].agg('sum')
    yearly_revenue_nolisc = datadf['rounded_revenue'].agg('sum')
    yearly_increased_tax_rev_21 = yearly_revenue_nolisc * .21
    # # -tax rev increase normal 30% -tax increase commercial 60% 
    # yearly_rev_nolisc_comm = datadfcomm['rounded_re'].agg('sum')
    # yearly_rev_nolisc_nocomm = datadfnocomm['rounded_re'].agg('sum')
    yearly_rev_nolisc_comm = datadfcomm['rounded_revenue'].agg('sum')
    yearly_rev_nolisc_nocomm = datadfnocomm['rounded_revenue'].agg('sum')
    yearly_rev_nocomm = (yearly_rev_nolisc_nocomm * .30)
    yearly_rev_comm = (yearly_rev_nolisc_comm * .60)
    yearly_rev_tot = yearly_rev_nocomm + yearly_rev_comm
    feestats.append(round(yearly_fee_tot,2))
    feestats.append(round(yearly_increased_tax_rev_21,2))
    feestats.append(round(yearly_rev_tot,2))
    return feestats

# feestats_list = feetax_stats(policy1_df0, policy1_df0_comm, policy1_df0_nocomm)


esri = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
attrib = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'

def original_airbnb_map(mapdf, tileinfo, attribinfo, filetitle):
    #create bubble map
    bub_map = folium.Map(location=[mapdf.latitude.mean(),mapdf.longitude.mean()], zoom_start=12, control_scale=True, tiles=tileinfo, attr=attribinfo) 
    folium.LayerControl().add_to(bub_map)
    #TODOD change 1 to yes and had total listings and if in florence and make more maps for commercial and not in florence 
    for index, location_info in mapdf.iterrows():
        folium.CircleMarker([location_info["latitude"],location_info["longitude"]], radius=2, color="black", fill=True, fill_color ="black",  popup="name: <br>" + str((location_info["name"])) + " hostname: <br> " + str(location_info["host_name"]) + " Commercial Property : <br> " + str(location_info["commercial"]) + " Price: <br>" + str(location_info["price"]), tooltip="yearly revenue: " + str(location_info["rounded_revenue"])).add_to(bub_map)
    
    bub_map.save('Out_Map/' + filetitle + '.html')
    return bub_map
#original_airbnb_map(mapdf, datadf, tileinfo)
# original_airbnb_map(df0, esri, attrib, 'original_airbnb_map')

esri = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
attrib = 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'

def updated_airbnb_map(mapdf, datadf, inverse_datadf, tileinfo, attribinfo, filetitle):
    #create updated bubble map after clicking certain policy x
    updated_bub_map = folium.Map(location=[mapdf.latitude.mean(),mapdf.longitude.mean()], zoom_start=12, control_scale=True, tiles=tileinfo, attr=attribinfo) 
    folium.LayerControl().add_to(updated_bub_map)
    
    #TODO maybe remove commercial or change 1 to yes and had total listings and if in florence 
    for index, location_info in datadf.iterrows():
        folium.CircleMarker([location_info["latitude"],location_info["longitude"]], radius=2, color="crimson", fill=True, fill_color ="crimson",  popup="name: <br>" + str((location_info["name"])) + " hostname: <br> " + str(location_info["host_name"]) + " Commercial Property : <br> " + str(location_info["commercial"]) + " Price: <br>" + str(location_info["price"]), tooltip="yearly revenue: " + str(location_info["rounded_revenue"])).add_to(updated_bub_map)
    
    for index, location_info in inverse_datadf.iterrows():
        folium.CircleMarker([location_info["latitude"],location_info["longitude"]], radius=2, color="blue", fill=True, fill_color ="blue",  popup="name: <br>" + str((location_info["name"])) + " hostname: <br> " + str(location_info["host_name"]) + " Commercial Property : <br> " + str(location_info["commercial"]) + " Price: <br>" + str(location_info["price"]), tooltip="yearly revenue: " + str(location_info["rounded_revenue"])).add_to(updated_bub_map)
    updated_bub_map.save('Out_Map/' + filetitle + '.html')

    return updated_bub_map
# updated_airbnb_map(df0, policy4_df0, policy4_df0_inverse, esri, attrib, 'policy4_df0_funct')



