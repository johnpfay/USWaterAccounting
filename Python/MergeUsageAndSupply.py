#MergeUsageAndSupply.py
#
# Joins the county level use and supply data and append readable state codes.
# Then summarizes values on state and saves as a tidy data table in csv format.
#
# Summer 2017
# John.Fay@duke.edu

#Load modules
import os
import pandas as pd
import numpy as np

#Set filenames
dataDir = '../Data'
usageFN = dataDir + os.sep + "AllUsageData.csv"
supplyFN = dataDir + os.sep + "SupplyData.csv"
stateFIPSFn = dataDir + os.sep + "FIPSstate.csv"
outFN = dataDir + os.sep + "UseAndSupply.csv"

#Create data frames from usage and supply
dfUsage = pd.read_csv(usageFN,dtype={'FIPS':np.str})
dfSupply = pd.read_csv(supplyFN,dtype={'FIPS':np.str})

#Add State FIPS codes columns
dfUsage['STFIPS'] = dfUsage['FIPS'].apply(lambda x: str(x)[:2] )
dfSupply['STFIPS'] = dfSupply['FIPS'].apply(lambda x: str(x)[:2] )

#Load state FIPS lookup table and join state codes
dfFIPS = pd.read_csv(stateFIPSFn,dtype=np.str)
dfSupply = pd.merge(dfSupply,dfFIPS,how='left',left_on='STFIPS',right_on='state_fips')
dfUsage = pd.merge(dfUsage,dfFIPS,how='left',left_on='STFIPS',right_on='state_fips')

#Compute supply as precip - et
dfSupply['SUPPLY'] = dfSupply['pr'] - dfSupply['et']

#Drop the FIPS from the tables
dfUsage.drop(['STFIPS','state_fips','FIPS'], axis=1, inplace = True)
#dfSupply.drop(['STFIPS','state_fips','FIPS','total_runoff','pr','et','smc'], axis=1, inplace = True)

#Group the supply table on state
grpSupply = pd.DataFrame(dfSupply.groupby(['YEAR','state'])['SUPPLY'].sum())

#Group the usage table on state
grpUsage = dfUsage.groupby(['YEAR','state']).sum()

#join tables on year and fips
dfX = pd.merge(grpSupply, grpUsage, how='outer',left_index=True,right_index=True)
dfX.to_csv(outFN,na_rep=0)

