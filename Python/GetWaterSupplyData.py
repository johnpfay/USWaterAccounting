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
import matplotlib

#Grab the FIPS data and create a dataframe from it
print "Getting record FIPS data"
fipsURL = "https://raw.githubusercontent.com/johnpfay/USWaterAccounting/VersionZero/Data/FIPS.csv"
dfFIPS = pd.read_csv(fipsURL)

#Initialize the output file and write the header line
print "Initializing the output file"
outFile = open("..\Data\HydroData.csv",'wt')
outFile.write("YEAR,LONGITUDE,LATITUDE,COFIPS,STFIPS,RUNOFF,PRECIP,ET,SME\n")

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
    dataDict = {}
    for url in (roURL, prURL, etURL, smURL):
        print "...downloading data from " + url
        #Retrieve the data file from the ftp server
        urllib.urlretrieve(url,"tmpData.nc")
        
        #Convert to netCDF object
        nc = netCDF4.Dataset("tmpData.nc",mode='r')
        
        #Add the lats and lons array to the dictionary
        dataDict["lats"] = nc.variables['latitude'][:]
        dataDict["lons"] = nc.variables['longitude'][:]
            
        #Get the parameter name and its values
        param_name = nc.variables.keys()[-1]
        param_vals = nc.variables.values()[-1]
        
        #Collapse the monthly values into a single array
        dataDict[param_name] = param_vals[:,:,:].sum(axis=0)
        
        #Close the nc object
        nc.close()
        
        #Delete the nc file
        os.remove("tmpData.nc")
        
        #Update
        urllib.urlcleanup()
        print "....complete"
        
    #Write array values as X,Y table
    #Create lons and lats array
    lons = dataDict["lons"]
    lats = dataDict["lats"]

    #Initialize the index to retrieve FIPS codes
    idxFIPS = 0

    for x in xrange(len(lons)):
        for y in xrange(len(lats)):
            #Get the runoff values, determine if it's masked or not
            ro = dataDict['total_runoff'][y,x]
            #Check if data is in the cell, skip to next if not
            if type(ro) is np.ma.core.MaskedConstant:
                continue
            #Get the FIPS codes
            coFips = dfFIPS['COFIPS'][idxFIPS]
            stFips = dfFIPS['STATEFIPS'][idxFIPS]
            idxFIPS += 1
            #Get the other values
            pr = dataDict['pr'][y,x]
            et = dataDict['et'][y,x]
            smc = dataDict['smc'][y,x]
            lon = lons[x]
            lat = lats[y]
            #Generate the output string and write it
            outStr = "{},{},{},{},{},{},{},{},{}\n".format(year,lon,lat,coFips,stFips,ro,pr,et,smc)
            outFile.write(outStr)
        
outFile.close()