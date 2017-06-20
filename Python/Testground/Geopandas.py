#https://gis.stackexchange.com/questions/175228/geopandas-spatial-join-extremely-slow
import sys, os
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame, read_file
from geopandas.tools import sjoin
from shapely.geometry import Point, mapping,shape

#parameters
dataDir = "..\\..\\Data"
countyFN = dataDir + os.sep + "cb_2016_us_county_500k.shp"
outFC = dataDir + os.sep + "mergedfoo.csv"
df=pd.read_csv(dataDir + os.sep + "HydroData.csv",index_col=None)#,nrows=2000) 

df['geometry'] = df.apply(lambda z: Point(z.LONGITUDE, z.LATITUDE), axis=1)
PointsGeodataframe = gpd.GeoDataFrame(df)
PolygonsGeodataframe = gpd.GeoDataFrame.from_file(countyFN)
PointsGeodataframe.crs = PolygonsGeodataframe.crs
merged=sjoin(PointsGeodataframe, PolygonsGeodataframe, how='left')
merged.drop(merged.columns[[9,10,11,12,13,17]],axis=1,inplace=True)
merged.to_csv(outFC,index=None,encoding ='utf8')
