#!/usr/bin/env python
# coding: utf-8

# ## Observations and Insights 

# 

# In[4]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import numpy as np
from scipy.stats import linregress
from sklearn import datasets

# Study data files
mouse_metadata_path = "data/Mouse_metadata.csv"
study_results_path = "data/Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)

# Combine the data into a single dataset
merged_df = pd.merge(mouse_metadata, study_results, on="Mouse ID")
merged_df.head()


# In[5]:


# Checking the number of mice in the DataFrame.
mice_count = merged_df['Mouse ID'].count()
mice_count


# In[6]:


# Getting the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
duplicate_mouse_ids = merged_df.loc[merged_df.duplicated(subset=['Mouse ID', 'Timepoint']),'Mouse ID'].unique()
duplicate_mouse_ids


# In[7]:


# Optional: Get all the data for the duplicate mouse ID. 
duplicate_mouse_data = merged_df.loc[merged_df["Mouse ID"] == "g989"]
duplicate_mouse_data


# In[8]:


# Create a clean DataFrame by dropping the duplicate mouse by its ID.
clean_study_data_complete = merged_df[merged_df['Mouse ID'].isin(duplicate_mouse_data)==False]
clean_study_data_complete.head()


# In[9]:


# Checking the number of mice in the clean DataFrame.
mice_count_clean = clean_study_data_complete['Mouse ID'].count()
mice_count_clean


# ## Summary Statistics

# In[10]:


# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen

# This method is the most straighforward, creating multiple series and putting them all together at the end.
mean = clean_study_data_complete.groupby('Drug Regimen')['Tumor Volume (mm3)'].mean()

median = clean_study_data_complete.groupby('Drug Regimen')['Tumor Volume (mm3)'].median()

variance = clean_study_data_complete.groupby('Drug Regimen')['Tumor Volume (mm3)'].var()

stdv = clean_study_data_complete.groupby('Drug Regimen')['Tumor Volume (mm3)'].std()

sem = clean_study_data_complete.groupby('Drug Regimen')['Tumor Volume (mm3)'].sem()

summary_df = pd.DataFrame({"Mean": mean, "Median": median, "Variance": variance, "Standard Deviation": stdv, "SEM": sem})

summary_df


# ## Bar Plots

# In[11]:


treatments = clean_study_data_complete.groupby('Drug Regimen')

treatments_mice_total = treatments['Mouse ID'].count()

treatment_chart = treatments_mice_total.plot(kind="bar", title="Number of Mice per Treatment")

treatment_chart.set_xlabel("Treatments")
treatment_chart.set_ylabel("Number of Mice")

plt.show()
plt.tight_layout()


# In[12]:


# Generate a bar plot showing the number of mice per time point for each treatment throughout the course of the study using pyplot.
treatments_matplot = clean_study_data_complete["Drug Regimen"].unique()
treatments_matplot


treatment_count = (clean_study_data_complete.groupby(["Drug Regimen"])["Mouse ID"].count())
treatment_count

x_axis = treatments_matplot
plt.figure(figsize=(12,5))
plt.bar(x_axis, treatment_count, color='y',alpha=0.5, align='center')


# ## Pie Plots

# In[13]:


# Generate a pie plot showing the distribution of female versus male mice using pandas
gender_df = pd.DataFrame(clean_study_data_complete.groupby(["Sex"]).count()).reset_index()
gender_df.head()


# In[14]:


gender_df = gender_df[["Sex","Mouse ID"]]
gender_df = gender_df.rename(columns={"Mouse ID": "Count"})
gender_df.head()


# In[15]:


plt.figure(figsize=(10,6))
ax1 = plt.subplot(121, aspect='equal')
gender_df.plot(kind='pie', y = "Count", ax=ax1, autopct='%1.1f%%', 
startangle=90, shadow=False, labels=gender_df['Sex'])


# In[16]:


# Generate a pie plot showing the distribution of female versus male mice using pyplot
gender_count = (clean_study_data_complete.groupby(["Sex"])["Age_months"].count())
gender_count


# In[17]:


labels = ["Females", "Males"]
colors = ["pink", "blue"]
explode = (0.1, 0)

plt.pie(gender_count, explode=explode, labels=labels, colors=colors,
        autopct="%1.1f%%", shadow=True, startangle=140)
plt.axis("equal")


# ## Quartiles, Outliers and Boxplots

# In[18]:


# Calculate the final tumor volume of each mouse across four of the most promising treatment regimens. Calculate the IQR and quantitatively determine if there are any potential outliers. 
sorted_df = clean_study_data_complete.sort_values(["Drug Regimen", "Mouse ID", "Timepoint"], ascending=True)

max_time_df = sorted_df.loc[sorted_df["Timepoint"] == 45]
max_time_df.head()


# In[19]:


#Capomulin
capomulin_df = max_time_df[max_time_df['Drug Regimen'].isin(['Capomulin'])]
#capomulin_df.head()

capomulin_list = capomulin_df.sort_values(["Tumor Volume (mm3)"], ascending=True)
capomulin_list = capomulin_list["Tumor Volume (mm3)"]
#capomulin_list

quartiles = capomulin_list.quantile([.25,.5,.75])
lowerq = quartiles[0.25]
upperq = quartiles[0.75]
iqr = upperq-lowerq

print(f"The lower quartile is: {lowerq}")
print(f"The upper quartile is: {upperq}")
print(f"The interquartile range is: {iqr}")
print(f"The the median is: {quartiles[0.5]} ")

lower_bound = lowerq - (1.5*iqr)
upper_bound = upperq + (1.5*iqr)
print(f"Values below {lower_bound} could be outliers.")
print(f"Values above {upper_bound} could be outliers.")


# In[20]:


fig1, ax1 = plt.subplots()
ax1.set_title('Final Tumor Volume with Capomulin Regimen')
ax1.set_ylabel('Final Tumor Volume (mm3)')
ax1.boxplot(capomulin_list)
plt.show()


# In[21]:


#Ramicane

ramicane_df = max_time_df[max_time_df['Drug Regimen'].isin(['Ramicane'])]
#ramicane_df.head()

ramicane_list = ramicane_df.sort_values(["Tumor Volume (mm3)"], ascending=True)
ramicane_list = ramicane_list["Tumor Volume (mm3)"]
#ramicane_list

quartiles = ramicane_list.quantile([.25,.5,.75])
lowerq = quartiles[0.25]
upperq = quartiles[0.75]
iqr = upperq-lowerq

print(f"The lower quartile is: {lowerq}")
print(f"The upper quartile is: {upperq}")
print(f"The interquartile range is: {iqr}")
print(f"The the median is: {quartiles[0.5]} ")

lower_bound = lowerq - (1.5*iqr)
upper_bound = upperq + (1.5*iqr)
print(f"Values below {lower_bound} could be outliers.")
print(f"Values above {upper_bound} could be outliers.")


# In[22]:


fig1, ax1 = plt.subplots()
ax1.set_title('Final Tumor Volume with Ramicane Regimen')
ax1.set_ylabel('Final Tumor Volume (mm3)')
ax1.boxplot(ramicane_list)
plt.show()


# In[23]:


#Infubinol

infubinol_df = max_time_df[max_time_df['Drug Regimen'].isin(['Infubinol'])]
#infubinol_df.head()

infubinol_list = infubinol_df.sort_values(["Tumor Volume (mm3)"], ascending=True)
infubinol_list = infubinol_list["Tumor Volume (mm3)"]
#infubinol_list

quartiles = infubinol_list.quantile([.25,.5,.75])
lowerq = quartiles[0.25]
upperq = quartiles[0.75]
iqr = upperq-lowerq

print(f"The lower quartile is: {lowerq}")
print(f"The upper quartile is: {upperq}")
print(f"The interquartile range is: {iqr}")
print(f"The the median is: {quartiles[0.5]} ")

lower_bound = lowerq - (1.5*iqr)
upper_bound = upperq + (1.5*iqr)
print(f"Values below {lower_bound} could be outliers.")
print(f"Values above {upper_bound} could be outliers.")


# In[24]:


fig1, ax1 = plt.subplots()
ax1.set_title('Final Tumor Volume with Infubinol Regimen')
ax1.set_ylabel('Final Tumor Volume (mm3)')
ax1.boxplot(infubinol_list)
plt.show()


# In[25]:


#Ceftamin

ceftamin_df = max_time_df[max_time_df['Drug Regimen'].isin(['Ceftamin'])]
#ceftamin_df.head()

ceftamin_list = ceftamin_df.sort_values(["Tumor Volume (mm3)"], ascending=True)
ceftamin_list = ceftamin_list["Tumor Volume (mm3)"]
#ramicane_list

quartiles = ceftamin_list.quantile([.25,.5,.75])
lowerq = quartiles[0.25]
upperq = quartiles[0.75]
iqr = upperq-lowerq

print(f"The lower quartile is: {lowerq}")
print(f"The upper quartile is: {upperq}")
print(f"The interquartile range is: {iqr}")
print(f"The the median is: {quartiles[0.5]} ")

lower_bound = lowerq - (1.5*iqr)
upper_bound = upperq + (1.5*iqr)
print(f"Values below {lower_bound} could be outliers.")
print(f"Values above {upper_bound} could be outliers.")


# In[26]:


fig1, ax1 = plt.subplots()
ax1.set_title('Final Tumor Volume with Ceftamin Regimen')
ax1.set_ylabel('Final Tumor Volume (mm3)')
ax1.boxplot(ceftamin_list)
plt.show()


# ## Line and Scatter Plots

# In[27]:


# Generate a line plot of time point versus tumor volume for a mouse treated with Capomulin
capo_df = clean_study_data_complete.loc[clean_study_data_complete["Drug Regimen"] == "Capomulin"]
#capo_df.head()

capo_single_df = capo_df.loc[capo_df["Mouse ID"] == "s185"]
#capo_single_df

capo_single_df = capo_single_df.loc[:, ["Timepoint", "Tumor Volume (mm3)"]]

capo_single_df.set_index('Timepoint').plot(figsize=(10, 8), linewidth=2.5, color='green')


# In[35]:


# Generate a scatter plot of mouse weight versus average tumor volume for the Capomulin regimen
scatter_data_df = capo_df.loc[:, ["Mouse ID", "Weight (g)", "Tumor Volume (mm3)"]]
#scatter_data_df.head()

mean_tumor_df = pd.DataFrame(scatter_data_df.groupby(["Mouse ID", "Weight (g)"])["Tumor Volume (mm3)"].mean()).reset_index()
#mean_tumor_df.head()

mean_tumor_df = mean_tumor_df.rename(columns={"Tumor Volume (mm3)": "Average Tumor Volume"})
mean_tumor_df.head()


# In[36]:


mean_tumor_df = mean_tumor_df.set_index('Mouse ID')


# In[38]:


mean_tumor_df.plot(kind="scatter", x="Weight (g)", y="Average Tumor Volume", grid=True, figsize=(4,4),
              title="Weight Vs. Average Tumor Volume")
plt.show()


# ## Correlation and Regression

# In[39]:


# Calculate the correlation coefficient and linear regression model 
# for mouse weight and average tumor volume for the Capomulin regimen
mouse_weight = mean_tumor_df.iloc[:,0]
avg_tumor_volume = mean_tumor_df.iloc[:,1]
correlation = st.pearsonr(mouse_weight,avg_tumor_volume)
print(f"The correlation between both factors is {round(correlation[0],2)}")


# In[41]:


x_values = mean_tumor_df['Weight (g)']
y_values = mean_tumor_df['Average Tumor Volume']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('Mouse Weight')
plt.ylabel('Average Tumor Volume')
plt.show()


# In[ ]:




