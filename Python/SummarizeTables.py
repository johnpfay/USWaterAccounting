
# coding: utf-8

# ## Summarize Tables
# * Joins FIPS codes to downloaded water tables and summarizes by state

# In[2]:


#import libraries
import sys, os
import pandas as pd
import numpy as np


# In[4]:


#get the filenames
dataDir = "../../Data"
fipsCSV = dataDir + os.sep + "FIPS.csv"
dataCSV = dataDir + os.sep + "Year2000.csv"
outCSV = dataDir + os.sep + "Year2000_byState.csv"


# In[9]:


#make data frames from the csv files
dfFIPS = pd.read_csv(fipsCSV)
dfData = pd.read_csv(dataCSV)
print dfFIPS.shape, dfData.shape


# In[27]:


dfData.columns


# In[20]:


#join FIPS to data
dfData['STATE'] = dfFIPS[' STATEFIPS']


# In[40]:


#Summarize on state  NOT WORKING
grpState = dfData[['Runoff', 'Precip', 'ET', 'SoilMoisture']].groupby(dfData['STATE']).mean()
grpState.to_csv(outCSV)

