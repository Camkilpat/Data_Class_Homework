#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# ----
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress
from pprint import pprint

# Import API key
from api_keys import weather_api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "../output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# ## Generate Cities List

# In[3]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# In[4]:


#checking output file
city_df = pd.read_csv(output_data_file)
city_df.head()


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

# In[5]:


#Creating list
city_name = []
cloudiness = []
country = []
date = []
max_temp = []
wind_speed = []
humidity = []
lat = []
lng = []
i = 0

#creating url
url = "http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID="
url_api = url + weather_api_key

#viewing info
weather_info = requests.get(url_api).json()
pprint(weather_info)


# In[6]:


print (f'-----------------------------')
print (f'Beginning Data Retrieval')
print (f'-----------------------------')

#loop through info
for city in cities:
    weather_data = requests.get(url_api + "&q=" + city + "&units=Imperial")
    weather_data_json = weather_data.json()
    
    #try to find the information
    try:
        city_name.append (weather_data_json ['city']['name'])
        country.append(weather_data_json['city']['country'])
        lat.append(weather_data_json['city']['coord']['lat'])
        lng.append(weather_data_json['city']['coord']['lon'])
        cloudiness.append (weather_data_json ['list'][0]['clouds']['all'])
        date.append(weather_data_json['list'][0]['dt'])
        humidity.append(weather_data_json['list'][0]['main']['humidity'])
        max_temp.append(weather_data_json['list'][0]['main']['temp_max'])
        wind_speed.append(weather_data_json['list'][0]['wind']['speed'])
        i += 1 
        print(f'Processing city {i} | {city}')
        
    except:
        print ('No City Located!')
        pass
    
print (f'-----------------------------')
print (f'End of Data Retrieval')
print (f'-----------------------------')


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[9]:


weather_dict = {
    "City": city_name,
    "Cloudiness" : cloudiness,
    "Country" : country,
    "Date" : date,
    "Humidity" : humidity,
    "Temp": max_temp,
    "Lat" : lat,
    "Lng" : lng,   
    "Wind Speed" : wind_speed
}
weather_df = pd.DataFrame(weather_dict)
weather_df.count()


# In[11]:


weather_df.head()


# In[13]:


weather_df.to_csv('../output_data/my_weather_data.csv')


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[22]:


scatlat = weather_df["Lat"]
scattemp = weather_df["Temp"]
plt.scatter(scatlat,scattemp)
plt.grid(color='gray', linestyle='-', linewidth=.5)
plt.xlabel('Latitude')
plt.ylabel('Max Temperature (F)')
plt.title('City Latitude vs. Max Temperature (04/18/2020)')
plt.savefig('../output_data/lat_vs_maxtemp.png')
plt.show()


# In[ ]:


# As latitude moves away from 0 the temperature decreases 


# #### Latitude vs. Humidity Plot

# In[30]:


humidity = weather_df["Humidity"]
plt.scatter(scatlat,humidity)
plt.grid(color='gray', linestyle='-', linewidth=.5)
plt.xlabel('Latitude')
plt.ylabel('Humidity (%)')
plt.title('City Latitude vs. Humidity (04/18/2020)')
plt.savefig('../output_data/lat_vs_humidity.png')
plt.show()


# In[ ]:


#Dont see a direct correlation with latitude and humidity. We can see a larger humidity percentage with increasing latitude. 


# #### Latitude vs. Cloudiness Plot

# In[37]:


cloudiness = weather_df["Cloudiness"]
plt.scatter(scatlat,cloudiness)
plt.grid(color='gray', linestyle='-', linewidth=.5)
plt.xlabel('Latitude')
plt.ylabel('Cloudiness (%)')
plt.title('City Latitude vs. Cloudiness (04/18/2020)')
plt.savefig('../output_data/lat_vs_cloudiness.png')
plt.show()


# In[ ]:


# no correlation between latitude and cloudiness percentage 


# #### Latitude vs. Wind Speed Plot

# In[43]:


wind_speed = weather_df["Wind Speed"]
plt.scatter(scatlat,wind_speed)
plt.grid(color='gray', linestyle='-', linewidth=.5)
plt.xlabel('Latitude')
plt.ylabel('Wind Speed (mph)')
plt.title('City Latitude vs. Wind Speed (04/18/2020)')
plt.savefig('../output_data/citylat_vs_windspeed.png')
plt.show()


# In[44]:


# Relative low windspeed at 0 latitude and increasing as you move from 0. 


# ## Linear Regression

# In[45]:


# OPTIONAL: Create a function to create Linear Regression plots


# In[46]:


# Create Northern and Southern Hemisphere DataFrames
nh_df = weather_df.loc[weather_df["Lat"] >= 0,:]
sh_df = weather_df.loc[weather_df["Lat"] < 0,:]

nh_df.head()


# ####  Northern Hemisphere - Max Temp vs. Latitude Linear Regression

# In[109]:





# ####  Southern Hemisphere - Max Temp vs. Latitude Linear Regression

# In[110]:





# ####  Northern Hemisphere - Humidity (%) vs. Latitude Linear Regression

# In[111]:





# ####  Southern Hemisphere - Humidity (%) vs. Latitude Linear Regression

# In[112]:





# ####  Northern Hemisphere - Cloudiness (%) vs. Latitude Linear Regression

# In[115]:





# ####  Southern Hemisphere - Cloudiness (%) vs. Latitude Linear Regression

# In[114]:





# ####  Northern Hemisphere - Wind Speed (mph) vs. Latitude Linear Regression

# In[117]:





# ####  Southern Hemisphere - Wind Speed (mph) vs. Latitude Linear Regression

# In[116]:





# In[ ]:




