#ReadUSGSData.py
#
# Description:
#  Accesses raw USGS water usage data and creates Numpy/Pandas table for analysis/visualization.
#  Provides the template for the following analyses:
#  - Merge data for 2000, 2005, and 2010 into a single data frame
#  - Aggregate county level data to the state level
#  - Generate state/county choropleth maps of different attributes
# 
# Summer 2017
# John.Fay@duke.edu

#Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Output file
outFN = "../Data/UseData.csv"

#Functions
def fix2000(df):
    '''Renames columns to match 2010 use table'''
    #Values to change
    inItems = ['IT-','LA-','LS-']#,'PE-']
    outItems = ['IC-','AQ-','LI-']#,'PT-']
    #Get column names
    colNames = df.columns.values
    #Convert to a list
    listNames = colNames.tolist()
    #For each inItem, change value in list
    for idx in range(len(inItems)):
        inVal = inItems[idx]
        outVal = outItems[idx]
        newList = [x.replace(inVal,outVal) for x in listNames]
        listNames = newList
    #Update column names
    df.columns = newList                  
    #Insert YEAR column
    df.insert(4,"YEAR",2000)
    return df

def fix2005(df):
    '''Renames columns to match 2010 use table'''
    #Values to change
    inItems = ['LA-','LS-']
    outItems = ['AQ-','LI-']
    #Get column names
    colNames = df.columns.values
    #Convert to a list
    listNames = colNames.tolist()
    #For each inItem, change value in list
    for idx in range(len(inItems)):
        inVal = inItems[idx]
        outVal = outItems[idx]
        newList = [x.replace(inVal,outVal) for x in listNames]
        listNames = newList
    #Update column names
    df.columns = newList                  
    #Insert YEAR column
    df.insert(4,"YEAR",2005)
    return df

#Create a master data frame from the yearly file/url
theBaseURL = 'http://water.usgs.gov/watuse/data/{0}/usco{0}.txt' #Use format to replace {0} with year
#Initialize list of year data frames
dfs = []

#Column data type dictionary (avoids converting FIPS to numeric types)
formatDict = {'STATEFIPS':str,'COUNTYFIPS':str,'FIPS':str}

#Year 2000
print "Getting year 2000 data"
df00 = pd.read_table(theBaseURL.format(2000),dtype=formatDict)
fix2000(df00)

#Year 2005
print "Getting year 2005 data"
df05 = pd.read_table(theBaseURL.format(2005,dtype=formatDict))
df05.drop(df05.columns.values[-1],axis=1,inplace=True)
fix2005(df05)

#Year 2010
print "Getting year 2010 data"
df10 = pd.read_table(theBaseURL.format(2010),dtype=formatDict)
df10.drop(df10.columns.values[-1],axis=1,inplace=True)

#Merge tables
print "Merging tables..."
df = pd.concat([df00,df05,df10])

#Fix FIPS columns
df['STATEFIPS'] = df['STATEFIPS'].apply(lambda x: str(x).zfill(2))
df['COUNTYFIPS'] = df['COUNTYFIPS'].apply(lambda x: str(x).zfill(3))
df['FIPS'] = df['FIPS'].apply(lambda x: str(x).zfill(5))

#Save file
df.to_csv(outFN,columns=df10.columns,index_label="KEY")

#Pivot on sector totals, by year
wdNames = ['YEAR','STATE','Public','Domestic','Industry','Irrigation','Livestock','Aquaculture','Mining','Thermo','zTOTAL']
wdFields = ['YEAR','STATE','PS-WFrTo','DO-WFrTo','IN-WFrTo','IR-WFrTo','LI-WFrTo','AQ-WFrTo','MI-WFrTo','PT-WFrTo','TO-WFrTo']
#df2000 = dfUsage[dfUsage.YEAR == 2000]
dfWithdrawals = df[wdFields]
dfWithdrawals.columns = wdNames
pv = dfWithdrawals[wdNames].pivot_table(index=('STATE','YEAR'),values=wdNames,aggfunc=np.sum).T
pv['NC'].to_csv("NC_usage.csv",index=True)

pv2000 = dfWithdrawals[wdNames].pivot_table(index=('STATE'),values=wdNames,aggfunc=np.sum).T
pv2000.to_csv("../Data/Usage2000.csv",index=True)
#Pivot values on year data by year and state
#pt = dfUsage.pivot_table(values='TP-TotPop',index='STATEFIPS',columns='YEAR',aggfunc=np.sum)
#pt.to_csv(outCSV)