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

The current version of this tool requires: (1) a template of the desired output: a physical supply and use table (PSUT) in the form of an Excel worksheet, and (2) a value mapping table that cross references the state usage attributes to the proper cell in the PSUT table. Examples of both are provided as part of this tool. 

### Current status

The USGS and the accountants continue to discuss the best format of the accounting tables given the data available. In response, we have adapted our code to include a level of flexibility in how it summarizes, transforms, and ultimately ports the data stored in the database tables into the specific spreadsheet cells to meet various format changes. 



## Products

All code is written in Python (version 2.7) and are available interactive Python (i.e, *IPython*) notebooks and as standalone Python scripts hosted on GitHub:<https://github.com/johnpfay/USWaterAccounting>. Each notebook/script is fully documented and requires no proprietary software. These products do, however,  require some 3rd party open-source packages to be installed prior to execution.

The IPython notebooks and the Python stand-alone scripts are redundant. The former is useful for walking through the individual scripting workflows to better understand the logic of the process. These notebooks, however, are not well suited to iterating (e.g. over all states), and so for batch running the analysis for all dates and for all years, we've also provided stand-alone Python scripts. 

### IPython Notebooks

IPython Notebooks show code along with formatted text in a readable and interactive document. The code (and text) are presented as blocks which can be viewed/run in a linear format. Thus, as mentioned above, the code does not lend itself to any sort of branching or looping, and therefore is best suited to demonstrate single examples of processing workflows, for example running one state's and one year's worth of data rather than looping through all states and all years. 

* `Scripts/RetrieveStateUsageData.ipynb` ([link](http://nbviewer.jupyter.org/github/johnpfay/USWaterAccounting/blob/master/Scripts/RetrieveStateUsageData.ipynb))- This notebook downloads water use data for a user specified state (e.g., Louisiana) and year (e.g. 2010) from the National Water Information System server, and translates these data into physical supply and use table (PSUT), using a preformatted PSUT template and value mapping table. 
* `Scripts/CompileStateUsageData.ipynb` ([link](http://nbviewer.jupyter.org/github/johnpfay/USWaterAccounting/blob/master/Scripts/CompileStateUsageData.ipynb)) - This notebook extracts data for all states for a given year and into a single CSV file. 

### Python Scripts

* `Scripts/CreateStatePSUTTables.py` - This script compiles 2000, 2005, and 2010 data for a given state into a set of three PSUT tables (one for each year). The state to process is set in line 26, and the output is stored as an Excel file in the Data/StateData folder as `xx_PSUTt.xlsx`, where `xx` is the state abbreviation. As the above `RetrieveStateUsageData.ipynb` notebook, this script requires the PSUT template and value mapping files. 
* `Scripts/CompileStateUsageData.py` - This script extracts data for all states for a given year and into a single CSV file. 

### Supplemental Data Files

These files are required to run the scripts. If kept in their original locations in the project workspace, the scripts should run as is; otherwise, the scripts should be edited to reflect new filename and/or locations. 

* `Data\Templates\StatePSUT_Template.xlsx` - This is the templates used to create all the statewide PSUT tables. This table can be reformatted any way with the important caveat that the `StatePSUTLookup.csv` file also be updates so that data values get mapped onto the correct cells. 
* `Data\RemapTables\StatePSUTLookup.csv` - This lists all the possible water use values stored in the statewide USGS water use datasets and the PSUT cell coordinate (column/row pair) into which the value should go. As some water usage categories are inserted into more than one cell - some in as many as three - in the PSUT, the value mapping file contains three sets of cell coordinates (i.e. column/row pairs). Thus, we repeat the process of reading the data frame and mapping values to the PSUT three times. In cases where two or more usage categories map to the same PSUT cell, the values will summed in the scripts that process this table.

### Discontinued IPython notebooks

Included in this project workspace are IPython notebooks used to process USGS nationwide usage data, the Louisiana SWUDS data example, and the CMIP-5 Hydrologic data (for water supply). We discontinued these efforts on deciding that the USGS statewide water use data had the best thematic resolution across the country. These notebooks were discontinued in various states of coding and may not be as stable as the above efforts. Consult the README.md file for a listing of what each notebook does; additional documentation are in the notebooks themselves. 

---



