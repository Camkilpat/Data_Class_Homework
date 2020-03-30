#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import csv


# In[2]:


total_votes = 0
khan_votes = 0
correy_votes = 0
li_votes = 0
otooley_votes = 0


# In[3]:


csvpath = os.path.join('Resources','election_data.csv')


# In[4]:


with open(csvpath, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ',')
    csv_header = next(csvfile)
    
    for row in csvreader:
        total_votes += 1
        
        if (row[2] == "Khan"):
            khan_votes += 1
        elif (row[2] == "Correy"):
            correy_votes += 1
        elif (row[2] == "Li"):
            li_votes += 1
        else:
            otooley_votes += 1
            
    kahn_percent = khan_votes / total_votes
    correy_percent = correy_votes / total_votes
    li_percent = li_votes / total_votes
    otooley_percent = otooley_votes / total_votes
    
    winner = max(khan_votes, correy_votes, li_votes, otooley_votes)
    
    if winner == khan_votes:
        winner_name = "Khan"
    elif winner == correy_votes:
        winner_name = "Correy"
    elif winner == li_votes:
        winner_name = "Li"
    else:
        winner_name = "O'Tooley" 


# In[6]:


output = (
    f"\nElection Results\n"
    f"------------------------\n"
    f"Total Votes: {total_votes}\n"
    f"------------------------\n"
    f"Kahn: {kahn_percent:.3%}({khan_votes})\n"
    f"Correy: {correy_percent:.3%}({correy_votes})\n"
    f"Li: {li_percent:.3%}({li_votes})\n"
    f"O'Tooley: {otooley_percent:.3%}({otooley_votes})\n"
    f"------------------------\n"
    f"Winner: {winner_name}\n"
    f"------------------------\n")


# In[7]:


print(output)


# In[8]:


output_file = os.path.join('Resources', 'election_data_revised.text')


# In[9]:


with open(output_file, "w") as txt_file:
    txt_file.write(output)


# In[ ]:




