import folium

# m = folium.Map()
map = folium.Map(location=[listings_location.latitude.mean(),listings_location.longitude.mean()], zoom_start=12, control_scale=True)

map.save("firenze_folium_map.html") 
map