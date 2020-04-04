#!/usr/bin/env python
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[25]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
PD = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(PD)
purchase_data.head()


# ## Player Count

# In[26]:


total_players = len(purchase_data["SN"].value_counts())
player_count = pd.DataFrame({"Total Players":[total_players]})
player_count


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[24]:


number_of_unique_items = len((purchase_data["Item ID"]).unique())
average_purchase_price = (purchase_data["Price"]).mean()
total_number_of_purchases = (purchase_data["Purchase ID"]).count()
total_revenue = (purchase_data["Price"]).sum()

summary_df = pd.DataFrame({"Number of Unique Items": [number_of_unique_items],
                          "Average Price": [average_purchase_price],
                          "Total Number of Purchases": [total_number_of_purchases],
                          "Total Revenue":[total_revenue]})
summary_df.style.format({'Average Price':"${:,.2f}"})
summary_df["Total Revenue"] = summary_df["Total Revenue"].map("${:,.2f}".format)
summary_df


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[35]:


gender_stats = purchase_data.groupby("Gender")

total_gender_count = gender_stats.nunique()["SN"]

percentage_of_players = total_gender_count / total_players * 100


gender_demographics = pd.DataFrame({"Total Count": total_gender_count,
                                    "Percentage of Players": percentage_of_players})

gender_demographics.sort_values(["Total Count"], ascending = False).style.format({"Percentage of Players":"{:.2f}%"})


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[38]:


purchase_count = gender_stats["Purchase ID"].count()

avg_purchase_price = gender_stats["Price"].mean()

avg_purchase_total = gender_stats["Price"].sum()

avg_purchase_per_person = avg_purchase_total/total_gender_count

gender_df = pd.DataFrame({"Purchase Count": purchase_count,
                          "Average Purchase Price": avg_purchase_price,
                          "Average Purchase Value":avg_purchase_total,
                          "Avg Purchase Total per Person": avg_purchase_per_person})

gender_df.index.name = "Gender"

gender_df.style.format({"Average Purchase Value":"${:,.2f}",
                        "Average Purchase Price":"${:,.2f}",
                        "Avg Purchase Total per Person":"${:,.2f}"})


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[53]:


bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
groups = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

purchase_data["Age Group"] = pd.cut(purchase_data["Age"],bins, labels=groups)
purchase_data

age_grouped = purchase_data.groupby("Age Group")

total_count_age = age_grouped["SN"].nunique()
 
percentage_by_age = (total_count_age/total_players) * 100

age_demographics = pd.DataFrame({"Total Count": total_count_age,
                                 "Percentage of Players": percentage_by_age})

age_demographics.index.name = None

age_demographics.style.format({"Percentage of Players":"{:,.2f}"})


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[60]:


age_purchase_count = age_grouped["Purchase ID"].count()

age_avg_purchase_price = age_grouped["Price"].mean()

total_purchase_value = age_grouped["Price"].sum()

avg_total_purchae_per_person = total_purchase_value/total_count_age

age_demographics = pd.DataFrame({"Purchase Count": age_purchase_count,
                                 "Average Purchase Price": age_avg_purchase_price,
                                 "Total Purchase Value":total_purchase_value,
                                 "Avg Total Purchase per Person": avg_total_purchae_per_person})

age_demographics.style.format({"Average Purchase Price":"${:,.2f}",
                               "Total Purchase Value":"${:,.2f}",
                               "Avg Total Purchase per Person":"${:,.2f}"})


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[66]:


spenders = purchase_data.groupby("SN")

spender_purchase_count = spenders["Purchase ID"].count()

spender_avg_purchase_price = spenders["Price"].mean()

spender_purchase_total = spenders["Price"].sum()

top_spenders = pd.DataFrame({"Purchase Count": spender_purchase_count,
                             "Average Purchase Price": spender_avg_purchase_price,
                             "Total Purchase Value":spender_purchase_total})

clean_spenders = top_spenders.sort_values(["Total Purchase Value"], ascending=False).head()

clean_spenders.style.format({"Average Purchase Total":"${:,.2f}",
                             "Average Purchase Price":"${:,.2f}",
                             "Total Purchase Value":"${:,.2f}"})


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[73]:


items = purchase_data[["Item ID", "Item Name", "Price"]]
 
item_stats = items.groupby(["Item ID","Item Name"])

item_purchase_count = item_stats["Price"].count()

purchase_value = (item_stats["Price"].sum()) 

item_price = purchase_value/purchase_count_item

most_popular_items = pd.DataFrame({"Purchase Count": item_purchase_count, 
                                   "Item Price": item_price,
                                   "Total Purchase Value":purchase_value})

clean_most_popular= most_popular_items.sort_values(["Purchase Count"], ascending=False).head()

clean_most_popular.style.format({"Item Price":"${:,.2f}",
                                "Total Purchase Value":"${:,.2f}"})


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[76]:


most_profitable_df = most_popular_items.sort_values(["Total Purchase Value"], ascending=False).head()

most_profitable_df.style.format({"Item Price":"${:,.2f}",
                                "Total Purchase Value":"${:,.2f}"})


# In[ ]:




