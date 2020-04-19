#!/usr/bin/env python
# coding: utf-8

# # VacationPy
# ----
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[50]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import gmaps
import os

# Import API key
from api_keys import g_key


# ### Store Part I results into DataFrame
# * Load the csv exported in Part I to a DataFrame

# In[51]:


#Read data and make dataframe
data = "../output_data/my_weather_data.csv"
weather_data = pd.read_csv(data)
weather_data
#weather_df = pd.DataFrame(weather_data)
#weather_df.head()


# ### Humidity Heatmap
# * Configure gmaps.
# * Use the Lat and Lng as locations and Humidity as the weight.
# * Add Heatmap layer to map.

# In[52]:


# Configure gmaps with API
gmaps.configure(api_key=g_key)


# In[53]:


# Store 'Lat' and 'Lng' into  locations 
locations = weather_df[["Lat", "Lng"]].astype(float)

weather_df = weather_df.dropna()

humidity_info = weather_df["Humidity"].astype(float)


# In[54]:


# Create a poverty Heatmap layer
fig = gmaps.figure()

heat_layer = gmaps.heatmap_layer(locations, weights=humidity_info, 
                                 dissipating=False, max_intensity=100,
                                 point_radius = 1)

fig.add_layer(heat_layer)

print(fig)


# ### Create new DataFrame fitting weather criteria
# * Narrow down the cities to fit weather conditions.
# * Drop any rows will null values.

# In[55]:


#A max temperature lower than 80 degrees but higher than 70.
first_cond = weather_df.loc[weather_df["Temp"]<80,:]

second_cond = first_cond.loc[weather_df["Temp"]>70,:]
#second_cond.head()

#Less than 10mph Wind
third_cond = second_cond.loc[second_cond["Wind Speed"]<10,:]

#Filtering to zero cloudiness.
fourth_cond = third_cond.loc[third_cond["Cloudiness"]==0,:]
fourth_cond.head()


# ### Hotel Map
# * Store into variable named `hotel_df`.
# * Add a "Hotel Name" column to the DataFrame.
# * Set parameters to search for hotels with 5000 meters.
# * Hit the Google Places API for each city's coordinates.
# * Store the first Hotel result into the DataFrame.
# * Plot markers on top of the heatmap.

# In[56]:


#Store into variable named hotel_df.
#Add a "Hotel Name" column to the DataFrame.
hotel_df = pd.DataFrame()
fifth_cond = pd.DataFrame(fourth_cond)
hotel_df['City'] = fifth_cond['City']
hotel_df['Country'] = fifth_cond['Country']
hotel_df['Lat'] = fifth_cond['Lat']
hotel_df['Lng'] = fifth_cond['Lng']
hotel_df['Hotel Name'] = ""
hotel_df.head()


# In[57]:


# use iterrows to scan dataframe
for index, row in hotel_df.iterrows():

    # get restaurant type from df
    lat = row['Lat']
    lng = row['Lng']
    city = row['City']
    country = row['Country']

    # assemble url and make API request
    print(f"Retrieving Results for Index {index}: {city}.")
    response = requests.get(f"https://maps.googleapis.com/maps/api/place/textsearch/json?location={lat},{lng}&radius=5000&type=hotel&key={g_key}").json()
    
    # extract results
    results = response['results']
    
    try:
        hotelname = response['results'][7]['name']
        print(f"Closest hotel to {city} at {lat} , {lng} is {hotelname}.")
        
        hotel_df.loc[index, "Hotel Name"] = hotelname
        
    except (KeyError, IndexError):
        print("Missing Information")
        
    print("------------")


# In[58]:


hotel_df.head()


# In[60]:


# NOTE: Do not change any of the code in this cell

# Using the template add the hotel marks to the heatmap
info_box_template = """
<dl>
<dt>Name</dt><dd>{Hotel Name}</dd>
<dt>City</dt><dd>{City}</dd>
<dt>Country</dt><dd>{Country}</dd>
</dl>
"""
# Store the DataFrame Row
# NOTE: be sure to update with your DataFrame name
hotel_info = [info_box_template.format(**row) for index, row in hotel_df.iterrows()]
locations = hotel_df[["Lat", "Lng"]]


# In[66]:


# Add marker layer ontop of heat map
fig = gmaps.figure()

heat_layer = gmaps.heatmap_layer(locations, weights = humidity_info, 
                                 dissipating=False, max_intensity=100,
                                 point_radius = 1)

marks = gmaps.marker_layer(locations)
fig.add_layer(heat_layer)
#fig.add_layer(marks)

# Display Map
fig


# In[ ]:




