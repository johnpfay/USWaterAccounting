#SummarizeWaterUseData.py
#
# Reads in the water supply table created via the GetWaterSupply.py script
# and computes total water supply at the state (or county) level by subtracting
# evapotranspiration from total rainfall.
#
# Summer 2017
# John.Fay@duke.edu

#Import libraries
import sys, os
import pandas as pd
import numpy as np

#Set the filenames
dataDir = "../Data"
dataFN = dataDir + os.sep + "HydroData.csv"
outFN = dataDir + os.sep + "StateSupply.csv"

#Read in the data
dfData = pd.read_csv(dataFN)
dfData['SUPPLY'] = dfData['PRECIP'] - dfData['ET']

#Summarize by state
grpState = dfData.groupby(('YEAR','STFIPS')).SUPPLY.sum()
grp2000 = dfData[dfData.YEAR==2000].groupby('STFIPS').SUPPLY.sum()
grp2005 = dfData[dfData.YEAR==2005].groupby('STFIPS').SUPPLY.sum()
grp2010 = dfData[dfData.YEAR==2010].groupby('STFIPS').SUPPLY.sum()

#Merge all years into a single data frame
dfAll = pd.concat((grp2000,grp2005,grp2000),axis=1)

#Rename the columns
dfAll.columns = ['y2000','y2005','y2010']

#Make sure FIPS has leading zeros
dfAll['FIPS']= dfAll.index.values
dfAll['FIPS'] = dfAll['FIPS'].apply(lambda x: str(x).zfill(2))

#Rearrange columns
dfAll = pd.DataFrame(dfAll,columns=['FIPS','y2000','y2005','y2010'])

#Export as csv
dfAll.to_csv(outFN,index_label='ID')