#BuildDataDict.py
#
# Description:
#  Accesses raw USGS water usage data and creates Numpy/Pandas table for analysis/visualization.
#  Provides the template for the following analyses:
#  - Merge data for 2000, 2005, and 2010 into a single data frame
#  - Aggregate county level data to the state level
#  - Generate state/county choropleth maps of different attributes
# 
# Summer 2017
# John.Fay@duke.edu

#Import modules
import pandas as pd

#Make data frames of each
df00 = pd.read_table("Data/DDict2000.txt")
df05 = pd.read_table("Data/DDict2005.txt")
df10 = pd.read_table("Data/DDict2010.txt")

#Change "Column Tag" name to year
df00.rename(columns={"Column Tag ":"year2000","Data Element":"D00"},inplace=True)
df05.rename(columns={"Column Tag ":"year2005","Data Element":"D05"},inplace=True)
df10.rename(columns={"Column Tag ":"year2010","Data Element":"D10"},inplace=True)

#Make known edits
#Make known edits
df00.replace(['IT-','LA-','LS-','PE-'],['IC-','AQ-','LI-','PT-'],inplace=True,regex=True)
df05.replace(['LA-','LS-'],['AQ-','LI-'],inplace=True,regex=True)

#Join all three on 'Data Element' field
#dfAll = pd.merge(df00,df05,how='outer',on='Data Element')
#dfAll = pd.merge(dfAll,df10,how='outer',on='Data Element')

dfAll = pd.merge(df10,df05,how='outer',left_on='year2010',right_on='year2005')
dfAll = pd.merge(dfAll,df00,how='outer',left_on='year2010',right_on='year2000')


#dfAll.columns.values.sort()
#dfAll.to_csv("Data/AllDict.csv",index=False)

dfAll[['year2010','year2005','year2000','D10','D05','D00']].to_csv("Data/AllDict.csv",index=False)