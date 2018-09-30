
# coding: utf-8

# # Byte 2: Tianwei Explore

# ## Preparation

# In[200]:


import csv
import httplib2
from apiclient.discovery import build
import urllib
import json

# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyCY5QazbQvs0YCrrUirdyFQtKObjZ2iFms'
# This is the table id for the fusion table
TABLE_ID = '1NUnXu2xO8ZaaHxtyYKhK2xMkUo2LxJergcjWDe1q'

try:
    fp = open("data.json")
    response = json.load(fp)
except IOError:
    service = build('fusiontables', 'v1', developerKey=API_KEY)
    query = "SELECT * FROM " + TABLE_ID #+ " WHERE AnimalType = 'DOG' LIMIT 10"
    response = service.query().sql(sql=query).execute()
    fp = open("data.json", "w+")
    json.dump(response, fp)
    
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


# ## Load Data

# In[201]:


#Then load the JSON data into a data frame:
df = pd.DataFrame(response[u'rows'], columns = response[u'columns'])
#and display a few rows to make sure everything works:
df.head(10)


# ## Data Cleaning

# In[202]:


### Drop NaN ### 
### The code below applies to_numeric() function to each column in the data frame, then removes all NaN values:
df = data_df.apply(lambda x: pd.to_numeric(x, errors='ignore')).dropna()

### Replace the unknow with 0 ### 
df = df.convert_objects(convert_numeric=True).fillna(0)
#data_df = data_df[['Huawei*']].convert_objects(convert_numeric=True).fillna(0)
df.head(10)


# In[203]:


### Drop the last (useless) column ### 
df = df.drop(df.columns[15], axis=1) #drop the last (useless) column
#df.ix[:, 15] = df.sum(axis=1)

### Check whether summation of the percentages of all brands sum up to be 1
Sum = df.sum(axis=1)
df.head(10)
#list(df.columns.values)


# ## Data Analysis

# In[204]:


### Correlation of Production of  Samsung and Apple ###

import seaborn as sns
pair_df = df[['Samsung','Apple']]
sns.jointplot(x="Samsung", y="Apple", data=pair_df);


# In[205]:


### Mean Production of each brand ###
df.mean(axis=0).plot(kind='bar', title='Bar chart of global market share held by leading smartphone vendors from 2009 to 2018')


# In[206]:


df.mean(axis=0).plot(kind='pie', title='Pie chart of global market share held by leading smartphone vendors from 2009 to 2018')


# In[207]:


df.mean(axis=0)[0:14]


# In[208]:


import matplotlib.pyplot as plt
N =  df.shape[0] # number of lines of df
ind = np.arange(N)   
val = df.columns.values

plt.bar(ind, df[val[0]])
bottom = df[val[0]]
for i in range(13):
    plt.bar(ind, df[val[i+1]], bottom=bottom)
    bottom += df[val[i+1]]

plt.ylabel('Percentage')
plt.title('Global market share held by leading smartphone vendors from 4th quarter 2009 to 2nd quarter 2018')
#xticks = ['Q4-09','Q1-10','Q2-10','Q3-10','Q4-10','Q1-11','Q2-11','Q3-11','Q4-11','Q1-12','Q2-12','Q3-12','Q4-12',
#                  'Q1-13','Q2-13','Q3-13','Q4-13','Q1-14','Q2-14','Q3-14','Q4-14','Q1-15','Q2-15','Q3-15','Q4-15',
#                  'Q1-16','Q2-16','Q3-16','Q4-16','Q1-17','Q2-17','Q3-17','Q4-17','Q1-18','Q2-18']
#plt.xticks(ind, xticks)

plt.show()

