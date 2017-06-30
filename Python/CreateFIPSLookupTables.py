#CreateFIPSLookupTables.py
#
#Retrieves a dataset of county-fips codes and creates two lookup tables:
# * Cross reference of FIPS code to county
# * Cross reference of 2digit FIPS code to state
#
# Summer 2017
# John.Fay@duke.edu

#Import modules
import os
import pandas as pd
import numpy as np

theURL =  'https://raw.githubusercontent.com/hadley/data-counties/master/county-fips.csv'
stateFN = '../Data/FIPSstate.csv'
countyFN = '../Data/FIPScounty.csv'

#Read in the data
df = pd.read_csv(theURL,dtype=np.str)

#Pad state_fips and county fips with zeros
df['state_fips'] = df['state_fips'].apply(lambda x: str(x).zfill(2))
df['county_fips'] = df['county_fips'].apply(lambda x: str(x).zfill(3))

#Combine state and county fips, padding where necessary
df['FIPS'] = df['state_fips'] + df['county_fips']

#Create county FIPS lookup table
dfCounty = df[['FIPS','state','county']]
dfCounty.to_csv(countyFN,index=False)

#Create the state FIPS lookup table
dfTmp = df[['state','state_fips']]
dfState = dfTmp.groupby(by='state_fips').first()
dfState.to_csv(stateFN,index_name="STFIPS")