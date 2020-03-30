#!/usr/bin/env python
# coding: utf-8

# In[41]:


import os
import csv


# In[42]:


total_months = 0
net_amount = 0
monthly_change = []
month_count = []
greatest_inc = 0
greatest_inc_month = 0
greatest_dec = 0
greatest_dec_month = 0


# In[43]:


csvpath = os.path.join('Resources', 'budget_data.csv')


# In[44]:


with open(csvpath, newline = '') as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ',')
    csv_header = next(csvreader)
    row = next(csvreader)
    
    previous_row = int(row[1])
    total_months += 1
    net_amount = net_amount + int(row[1])
    greatest_inc = int(row[1])
    greatest_month_inc = row[0]

    for row in csvreader:
        total_months += 1
        net_amount += int(row[1])
        
    revenue_change = int(row[1]) - previous_row
    monthly_change.append(revenue_change)
    previous_row = int(row[1])
    month_count.append(row[0])
    
    if int(row[1]) > greatest_inc:
        greatest_inc = int(row[1])
        greatest_inc_month = row[0]
    
    if int(row[1]) < greatest_dec:
        greatest_dec = int(row[1])
        greatest_dec_month = row[0]


# In[45]:


average_change = sum(monthly_change)/len(monthly_change)


# In[46]:


highest = max(monthly_change)
lowest = min(monthly_change)


# In[47]:


output = (
    f"\nFinancial Analysis\n"
    f"---------------------------\n"
    f"Total Months: {total_months}\n"
    f"Total: ${net_amount}\n"
    f"Average Change: ${average_change:.2f}\n"
    f"Greatest Increase in Profits: {greatest_inc_month},(${highest})\n"
    f"Greatest Decrease in Profits: {greatest_dec_month},(${lowest})\n")


# In[48]:


print(output)


# In[49]:


output_file = os.path.join('Resources','budget_data_revised.text')


# In[50]:


with open(output_file, "w") as txt_file:
    txt_file.write(output)

