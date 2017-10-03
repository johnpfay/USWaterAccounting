'''
Compile State Usage Data

Loops through a list of all states an pulls USGS water use data for each state into a single table.
Requires: pandas and us (installed via pip)

September 2017
John.Fay@Duke.edu
'''

#Import modules
from __future__ import print_function
import sys, os, urllib
import pandas as pd
from us import states

#Create the output csv file
outFilename = "../Data/AllStatesUsage2010.csv"

def getData(state_abbr,year=2010):
    '''Downloads USGS data and creates a tidy dataframe of all the usage data for the state'''
    
    #Set the data URL path and parameters and construct the url
    path = 'https://waterdata.usgs.gov/{}/nwis/water_use?'.format(state_abbr)
    values = {'format':'rdb',
             'rdb_compression':'value',
             'wu_area':'County',
             'wu_year': year,
             'wu_county':'ALL',
             'wu_county_nms':'--ALL+Counties--',
             'wu_category_nms':'--ALL+Categories--'
            }
    url = path + urllib.urlencode(values)
    
    #Pull data in using the URL and remove the 2nd row of headers
    dfRaw = pd.read_table(url,comment='#',header=[0,1],na_values='-')
    dfRaw.columns = dfRaw.columns.droplevel(level=1)

    #Tidy the data: transform so data in each usage column become row values with a new column listing the usage type
    rowHeadings = ['county_cd', 'county_nm', 'state_cd', 'state_name', 'year']
    dfTidy = pd.melt(dfRaw,id_vars=rowHeadings,value_name='MGal',var_name='Group')

    #Remove rows that don't have volume data (i.e. keep only columns with 'Mgal' in the name)
    dfTidy = dfTidy[dfTidy['Group'].str.contains('Mgal')].copy(deep=True)

    #Change the type of the MGal column to float 
    dfTidy['MGal'] = dfTidy.MGal.astype('float')
    
    #Summarize county data for the whole state
    stateSummary = dfTidy.groupby(['Group'])['MGal'].sum()
    
    #Convert to a dataframe
    dfState = pd.DataFrame(stateSummary)
    
    #Rename the MGal column to the state abbreviation
    dfState.columns = [state_abbr]
    
    #Return the dataframe
    return dfState

#Get the data for the first state
abbr = states.STATES_CONTINENTAL[0].abbr
print("Processing {}".format(abbr),end=" ")
dfAll = getData(abbr)

#Loop through states
for state in states.STATES_CONTINENTAL[1:]:
    abbr = state.abbr
    print("{}".format(abbr),end=" ")
    dfState = getData(abbr)
    dfAll = pd.merge(dfAll,dfState,how='inner',left_index='Group',right_index='Group')

dfAll.to_csv(outFilename)