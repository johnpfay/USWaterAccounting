#AssignFIPSArcPy.py
#Assigns the county FIPS code to each XY record in a csv file

import sys, os, csv
import arcpy
import numpy as np

arcpy.env.overwriteOutput = True

#County shapefile
countyFC = "../Data/cb_2016_us_county_500k.shp"

#CSV file
csvFile = "../Data/Year2000.csv"

#Create a pointFC from the CSV file
xyEventLayer = arcpy.MakeXYEventLayer_management(csvFile,"Longitude","Latitude","XY_Lyr")

#Create a feature class from the event layer
xyFeatureClass = arcpy.CopyFeatures_management(xyEventLayer,"in_memory/XYFeatures")

#Spatial join with countyFC
outJoinFC = "in_memory/JoinFC"
joinFC = arcpy.SpatialJoin_analysis(xyFeatureClass,countyFC,outJoinFC)

#Convert table to numpy array (Set null values to -1)
nullDict = {'GEOID':-1,'STATEFP':-1}
np1 = arcpy.da.TableToNumPyArray(joinFC,['GEOID','STATEFP'],null_value=nullDict)

#Combine the GEOID and STATEFP into a 2d array
npX = np.vstack([np1["GEOID"], np1["STATEFP"]])

#Write to a file
np.savetxt("../Data/FIPS.csv",
           npX.T,delimiter=',',
           fmt='%s',
           header=u"COFIPS, STATEFIPS"))

np0 = np.genfromtxt(csvFile,delimiter=",",skip_header=True)