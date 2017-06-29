# GetWaterSupplyData.py
#
# Description:
# * Downloads downscaled CMIP5 hydrology projection data from a central repository.
#   The file contains a year's worth of runoff, precipitation, evaportranspiration, and
#   soil moisture content data at 1/8th degree spatial resolution, measured monthly.
#
# * Monthly data for a given year are aggregated into annual sums and linked with a
#   listing of state and county FIPS codes for additional [spatial] aggregation.
#
# * The output is a table with a row for each point record (1/8th degree) listing:
#   YEAR: the year sampled (2000, 2005, 2010)
#   LONGITUDE:
#   LATITUDE:
#   COFIPS: the county FIPS code in which the record resides
#   STFIPS: the state FIPS code in which the record resides
#   RUNOFF: total annual runoff mm/year (sum of monthly values)
#   PRECIP: total annual precipitation mm/year
#   ET: total annual evapotranspiration
#   SME: total annual soil moisture content
#
# Currently the script is set to use the NCAR CCSM4 (2.6) model. This can be changed by
# modifying the ftp urls. See the documentation linked in the README.MD file.
#
# This script requires the FIPS.csv file which is created using the AssignFipsArcPy.py script
#
# Summer 2017
# John.Fay@duke.edu

#Import libraries
import sys, os, glob, time, datetime, urllib
import numpy as np
import pandas as pd
import netCDF4

#Get the FIPS filename and set the output filename
fipsFN = '../Data/FIPS.csv'
outFN = '../Data/SupplyData.csv'

#Create a dataframe of FIPS codes to join
dfFIPS = pd.read_csv(fipsFN,dtype=np.str)

#Set the year to process
for year in (2000,2005,2010):
    print "Processing year {}".format(year)

    #Get urls for NCAR 2.6 scenario ensembles: runoff(ro), precipitation(pr), evapotranspiration(et), soil moisture (sm)
    baseURL = 'ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/cmip5/hydro/BCSD_mon_VIC_nc/ccsm4_rcp26_r1i1p1/'
    baseURL2 = 'ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/cmip5/hydro/BCSD_mon_forc_nc/ccsm4_rcp26_r1i1p1/'
    roURL = baseURL + "conus_c5.ccsm4_rcp26_r1i1p1.monthly.total_runoff.{}.nc".format(year)
    prURL = baseURL2 + "conus_c5.ccsm4_rcp26_r1i1p1.monthly.pr.{}.nc".format(year)
    etURL = baseURL + "conus_c5.ccsm4_rcp26_r1i1p1.monthly.et.{}.nc".format(year)
    smURL = baseURL + "conus_c5.ccsm4_rcp26_r1i1p1.monthly.smc.{}.nc".format(year)

    #These lines fix an issue with slow network connections
    import socket
    socket.setdefaulttimeout(30)

    #Loop through each file and create an annual sum array; add it to a dictionary
    for url in (roURL, prURL, etURL, smURL):
        print "...downloading data from " + url
        #Retrieve the data file from the ftp server
        urllib.urlretrieve(url,"tmpData.nc")
        
        #Convert to netCDF object
        nc = netCDF4.Dataset("tmpData.nc",mode='r')
        
        #Get the parameter name and its values
        param_name = nc.variables.keys()[-1]
        param_vals = nc.variables.values()[-1]
        
        #Collapse the monthly values into a single 3d data frame
        dfParam = pd.DataFrame(param_vals[:,:,:].sum(axis=0))
        
        #Create latitude and longitude arrays (for the first element only)
        if url == roURL:
            dfLats = pd.DataFrame(nc.variables['latitude'][:])
            dfLons = pd.DataFrame(nc.variables['longitude'][:])
            
        #Close the nc object
        nc.close()
        
        #Delete the nc file
        os.remove("tmpData.nc")
        
        #Update
        urllib.urlcleanup()
        print "....complete"

        #Melt the data into a 3 column, 2d data frame
        dfParam.columns = dfLons[0].values.tolist() #Set column names to longitudes
        dfParam['LAT'] = dfLats[0].values.tolist()  #Add column of longitudes
        df = pd.melt(dfParam,id_vars=['LAT'],var_name='LON',value_name=param_name)

        #Append to dataframe, if not the first element
        if url == roURL:
            #Copy to the year dataframe
            dfYear = df.copy(deep=True)
            #Append fips values from FIPS dataframe
            dfYear['FIPS'] = dfFIPS.COFIPS
        else:
            #Add column to the year data frame
            dfYear[param_name] = df[param_name]
            
    #Add year to the master data frame
    dfYear.insert(1,'YEAR',year)

    #Append the year dataframe to the output dataframe, if not the first
    if year == 2000:
        dfAllYears = dfYear.copy(deep=True)
    else:
        dfAllYears = dfAllYears.append(dfYear)

#Remove records with no data (usually ones outside of US)
dfAllYears.dropna(inplace=True)

#Remove records with no FIPS code (-1)
dfAllYears = dfAllYears[dfAllYears.FIPS != "-1"]

#Drop lat and lon columns
dfAllYears.drop((['LAT','LON']),axis=1,inplace=True)

#Fix FIPS values to have leading zeros where appropriate
dfAllYears['FIPS'] = dfAllYears['FIPS'].apply(lambda x: str(x).zfill(5))

#Group data by county, summing the parameters
dfCounty = dfAllYears.groupby(('YEAR','FIPS')).sum()

#Write to file
dfCounty.to_csv(outFN)
