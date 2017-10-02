# US Water Accounting Data Project


### Project Scope and Objective:

Our objectives were to integrate various water accounting datasets identified by the USGS into a central database that facilitates update, management, query, and visualization. Additionally, we would provide code to automate the update, reformatting, and transformation of the raw data into this database. A final product would be water balance reports for select years (2000, 2005, and 2010) in a format defined by USGS. 



### Workflow milestones:

#### Dataset identification

The USGS identified one national source of water use accounting, namely the USGS Water Use dataset (<https://water.usgs.gov/watuse/>). We searched for and identified the CMIP5 Variable Infiltration Capacity (VIC) Macroscale Hydrologic Model output (<http://vic.readthedocs.io/>) as a potential national water supply dataset to complement the USGS use data. We also obtained an example of the Specific Water-Use Data System (SWUDS) statewide dataset from the Louisiana USGS office. 

After some deliberation, we settled on using USGS statewide datasets (e.g. https://waterdata.usgs.gov/la/nwis/wu). These data provided the richest thematic resolution that was standard across the nation. 

#### Code development for database assembly and management

Once we decided on the datasets, we developed a set of Python scripts to pull raw data directly from the on-line resources for a user specified year and synthesize these data into a set of core tables that would facilitate selection and query.  Inconsistencies in the water use data format across years required us to write code to standardize field names before merging data. Additionally, we wrote code to spatially aggregate water supply data, which were distributed in a 1/8° geographic grid, into county level values. 

#### Code development for database query and output formatting

After conversations with Michael Vardon, Julie Hass, and other environmental-economic accountants, we made initial attempts at a suitable format for the physical use-supply tables in which to present our data. We developed code to query and transform the database developed above into this format. 



### Current status

The USGS and the accountants continue to discuss the best format of the accounting tables given the data available. In response, we have adapted our code to include a level of flexibility in how it summarizes, transforms, and ultimately ports the data stored in the database tables into the specific spreadsheet cells to meet various format changes. 





## Deliverables

All code is written in Python (version 2.7) and are available as standalone Python scripts and/or interactive Python (i.e, IPython) notebooks hosted on GitHub:<https://github.com/johnpfay/USWaterAccounting>. Each script/notebook is fully documented and requires no proprietary software. These scripts do, however,  require some 3rd party open-source packages to be installed prior to execution.

The IPython notebooks and the Python stand-alone scripts are somewhat redundant. The former is useful for walking through the individual scripting workflows to better understand the logic of the process. These notebooks, however, are not well suited to iterating (e.g. over all states), and so for batch running the analysis for all dates and for all years, we've also provided stand-alone Python scripts. 

### IPython Notebooks

IPython Notebooks provide 

* `RetrieveStateUsageData.ipynb` - This notebook downloads water use data for a user specified state and year from the National Water Information System server, and translates these data into physical supply and use table (PSUT), using a preformatted PSUT template and value mapping table. 