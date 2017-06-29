#GetWaterUseData.py
#
# Import USGS use data & Create usage table
#
# Here we download the raw usage data for years 2000, 2005, and 2010 from the USGS usage site and synthesize all data into a flat table listing: year, FIPS code, and total annual withdrawals by sector in MGal/day (*so these need to be ajdusted for yearly sums!)
# 
# The steps required include:
# * Pulling the raw data file, in tab-delimted format, from the USGS server into a pandas dataframe.
# * Adjusting field names so that merging tables is seamless. This includes:
#     * Adding year columns to 2000 and 2005 datasets.
#     * For year 2000, remapping 'IT', 'LA', 'LS', and 'PE' fields to 'IC', 'AQ', 'LI' and 'PC', respectively([reference]( https://water.usgs.gov/watuse/data/2000/datadict.html)).
#         * IT -> IC (Irrigated cropland)
#         * LA -> AQ (Aquaculture)
#         * LS -> LI (Livestock)
#         * PE -> PC (Thermoelectric power closed-loop)
#     * For year 2005, remapping 'LA' and 'LS' fields to 'AQ' and 'LI', respectively([reference]( https://water.usgs.gov/watuse/data/2005/datadict.html)). 
#         * LA -> AQ (Aquaculture)
#         * LS -> LI (Livestock)
#     * Also need to fix inconsistencies in 'WTot' vs 'Wtot'
# * Concatenating all dataframes into a single dataframe, with records tagged by the year of the dataset.
# * Removing extraneous fields, keeping only the sector total columns:
#     * Care must be taken that the FIPS codes are preserved as text, not numbers
#      
# This table and then be joined, by FIPS code, to other accounting data tables and summarized by state.
#
# Summer 2017
# John.Fay@duke.edu

#Import modules
import os
import pandas as pd
import numpy as np

#Set the output location and filename
dataDir = '../Data'
outFN = dataDir + os.sep + 'AllUsageData.csv'

#Define the function to retrieve data and fix field name issues
def getData(year):
    print "Retrieving data for {}".format(year)
    
    #Create a dictionary of proper dtypes (avoids converting FIPS to numeric types)
    formatDict = {'STATEFIPS':str,'COUNTYFIPS':str,'FIPS':str}

    #Set the base URL to be used to get any annual dataset
    theBaseURL = 'http://water.usgs.gov/watuse/data/{0}/usco{0}.txt' 
    
    #Retrieve the data
    df = pd.read_table(theBaseURL.format(year),dtype=formatDict)
    
    #Remap the IT-, LA-, and LS- columns to IC-, AQ-, and LI-
    fldsIn = ('IT-','LA-','LS-','PE','Wtotl')
    fldsOut = ('IC-','AQ-','LI-','PC','WTotl')

    #Get the current column names as a list
    colNames = df.columns.values.tolist()

    #Create a revised column name list
    for inFld,outFld in zip(fldsIn,fldsOut):
        #This loops through each item in colNames and replaces it with a revised one
        colNames_update = [x.replace(inFld,outFld) for x in colNames]
        colNames = colNames_update

    #Update the column names in the data frame
    df.columns = colNames
    
    #Add year field, if not present
    if "YEAR" not in df.columns.values: 
        df.insert(4,"YEAR",year)
        
    #Remove unnamed columns
    if "Unnamed" in df.columns.values[-1]:
        df.drop(df.columns.values[-1],axis=1,inplace=True)
        
    #Return the updated dataframe
    return df

#Retrieve the data into a dataframe
df2000 = getData(2000)
df2005 = getData(2005)
df2010 = getData(2010)

#Merge the tables into one
df = pd.concat([df2000, df2005,df2010])

#Subset and rename columns (FRESH WATER ONLY)

#Create lists of columns to keep and names to assign
useFields = ['YEAR','FIPS','PS-WFrTo','DO-WFrTo','IN-WTotl','IR-WFrTo','LI-WFrTo','AQ-WFrTo','MI-WFrTo','PT-WFrTo','TO-WFrTo']
useNames = ['YEAR','FIPS','Public','Domestic','Industry','Irrigation','Livestock','Aquaculture','Mining','Thermoelectic','TOTAL']

#Subset columns in the list
dfUsage = df[useFields]

#Rename the columns
dfUsage.columns = useNames

#Fix FIPS column to include leading zeros
dfUsage['FIPS'] = df['FIPS'].apply(lambda x: str(x).zfill(5))

#Save as a CSV file
dfUsage.to_csv(outFN,index=False)


