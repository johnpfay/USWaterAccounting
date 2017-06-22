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
dtypeDict
dfData = pd.read_csv(dataFN)
dfData['SUPPLY'] = dfData['PRECIP'] - dfData['ET']

#Adjust columns in dataframe (FIPS and YEAR)
dfData.,c

#Pivot by state, summing by year
pv = dfData.pivot_table(index=('STFIPS'),columns=('YEAR'),values=('SUPPLY'),aggfunc=np.sum)

#Fix FIPS column
pv['FIPS'] = pv.index.values
pv['FIPS'] = pv['FIPS'].apply(lambda x: str(x).zfill(2))

#Rearrange columns
pv = pd.DataFrame(pv,columns=['FIPS','2000','2005','2010'])

#Export as csv
pv.to_csv(outFN,index_label='ID')