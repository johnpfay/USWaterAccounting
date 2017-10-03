### Overview of iPython notebooks

These iPython notebooks are developed to run in Python 2.7 using the Jupyter notebooks module. To install Juptyer notebooks, open a DOS command line in the Python scripts folder and run the following command:

`pip install jupyter`

Once it's installed, you should be able to double click the Jupyter shortcut located in the Python folder of this repository. If the shortcut is unable to locate the source, open the shortcut properties and check the path to your Python installation. 

* <u>CreateUsageTable.ipynb</u>

  Pulls national water usage data from USGS for 2000/2005/2010 from the USGS data portal, then combines and rearranges the data into a table listing year, county, usage class (e.g. irrigation, industry, livestock), source class (surface or groundwater), source type (fresh or saline), and amount (MGal/day). The output is written to `UsageDataTidy.csv` in the Data folder.

  ​

* <u>CreastSupplyTable.ipynb</u>

  Pulls hydrologic data (precipitation, evapotranspiration, soil moisture content, and runoff) for 2000/2005/2010 from a climate modeling repository. Assigns county FIPS codes to each data point, and then spatially aggregates the data by county across the US to generate a table of county water supply for each year. This script generates two outputs written to the Data folder: The SupplyTableTidy.csv lists 

  NOTE: This script requires a the geopandas package. A separate doc is being prepared with instructions how to install it. 

  ​

* <u>SummarizeTidyTables.ipynb</u>

  This script merges the usage and supply tables above to create a series of tables. These outputs include:

  * `WaterByCounty.csv`: A list of use and supply, summarized by county. 

  * `WaterByState.csv`: A list of use and supply, summarized by state.

  * `WaterBalanceData.csv`: A list of use and supply, summarized for the entire US.

    ​


* <u>FillExcelSpreadsheet.ipynb</u>

  This script takes the output from the SummarizeTidyTables.ipynb script, namely the WaterBalanceData.csv and fills in values in a formatted physical water use and supply spreadsheet, defined by the template file USWaterBalanceSheet.xlsx.

  ​

* <u>ConvertSWUDSToBalanceSheet.ipynp</u>

  This extracts values from the SWUDS.xlsx spreadsheet provided by Pierre Sargent (USGS), extracts values for 2000/2005/2010 and pivots the results so that SIC codes appear as rows and there is a column listing the usage volume for each year, and then inserts appropriate values in a preformatted use and supply table. 

  ​

* <u>LouisianaOnline.ipynb</u>

  Rather than use state SWUDS data, this script pulls state use data from the USGS server and tidy's it, writing the output to \<xx\>.csv where \<xx\> is the two digit state. 