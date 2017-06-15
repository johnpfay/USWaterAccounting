# #### Downscaled Climate Projections Archive processing
# ###### Workflow
# * Submit data request
# * Download data to data folder
# * Process NetCDF files into dataframes
# * Compute annual means (2000, 2005, and 2010) from monthly data
# * Compute means for each state


#Import libraries
import sys, os, glob, time, datetime, urllib
import numpy as np
import pandas as pd
import netCDF4
import matplotlib

#Get urls for NCAR 2.6 scenario ensembles: runoff(ro), precipitation(pr), evapotranspiration(et), soil moisture (sm)
year = 2000
baseURL = 'ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/cmip5/hydro/BCSD_mon_VIC_nc/ccsm4_rcp26_r1i1p1/'
baseURL2 = 'ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/cmip5/hydro/BCSD_mon_forc_nc/ccsm4_rcp26_r1i1p1/'
roURL = baseURL + "conus_c5.ccsm4_rcp26_r1i1p1.monthly.total_runoff.{}.nc".format(year)
prURL = baseURL2 + "conus_c5.ccsm4_rcp26_r1i1p1.monthly.pr.{}.nc".format(year)
etURL = baseURL + "conus_c5.ccsm4_rcp26_r1i1p1.monthly.et.{}.nc".format(year)
smURL = baseURL + "conus_c5.ccsm4_rcp26_r1i1p1.monthly.smc.{}.nc".format(year)

#Loop through each file and create an annual sum array; add it to a dictionary
dataDict = {}
for url in (roURL, prURL, etURL, smURL):
    print "Processing " + url
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
#Export as table of x,y, et
outFile = open("..\Data\Year{}.csv".format(year),'wt')
#Write headers
outFile.write("Longitude,Latitude,Runoff,Precip,ET,SoilMoisture\n")
for x in xrange(len(lons)):
    for y in xrange(len(lats)):
        ro = dataDict['total_runoff'][y,x]
        #Check if data is in the cell, skip to next if not
        if type(ro) is np.ma.core.MaskedConstant:
            continue
        pr = dataDict['pr'][y,x]
        et = dataDict['et'][y,x]
        smc = dataDict['smc'][y,x]
        lon = lons[x]
        lat = lats[y]
        outStr = "{},{},{},{},{},{}\n".format(lon,lat,ro,pr,et,smc)
        outFile.write(outStr)
outFile.close()