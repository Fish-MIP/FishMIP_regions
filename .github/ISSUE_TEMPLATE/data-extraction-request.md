---
name: Data extraction request
about: Request environmental data from Earth System Models to force your ecosystem
  model
title: Data extraction request
labels: ''
assignees: lidefi87

---

You can submit this request if you need environmental data from FishMIP approved Earth System Models (ESMs) to force your ecosystem model. Please make sure you complete this form as best as you can so we can extract the correct data for you.

Note that outputs from GFDL-MOM6-COBALT2 have been extracted for participating FishMIP regional models and are available via our [THREDDS server](http://portal.sf.utas.edu.au/thredds/catalog/gem/fishmip/catalog.html) and our [regional inputs shiny app](https://rstudio.global-ecosystem-model.cloud.edu.au/shiny/FishMIP_Input_Explorer/). If data is **NOT** available in either of these, you can submit a request for data to be extracted.

**Have you check the THREDDS server and then FishMIP input explorer?**
Ensure you check these two sources before submitting this request.

**Do you need data to be extracted for the entire globe or a specific region?**
If it is for the entire globe, skip the next two questions as they apply for the regions only.

**Have you submitted the spatial boundaries for your model to the FishMIP regional team?**
If you are unsure, check the map in this [page](https://github.com/fish-MIP/FishMIP_regions). If your regions is **NOT** in that map, you will need to get in touch with the [FishMIP regional coordinators](mailto:fishmip.coordinators@gmail.com).

**If you have submitted the spatial boundaries for your model, what is the name of your model?**
If the name of your model does **NOT** match the name in our map, please provide the name as it appears in our map and the correct name. We will update the name for you.

**What FishMIP protocol are you following?**
We currently have two protocols: 3a and 3b, if unsure, you can find more information [here](https://fishmip.org/protocols.html).

**What ESM should we extract data from?**
Note that protocol 3a has only one ESM available (GFDL-MOM6-COBALT2), but there two options with 3b (GFDL-ESM4 and IPSL-CM6A-LR).

**What ESM experiment should we extract data from?**
Options available: obsclim or ctrlclim.

**What ESM scenario should we extract data from?**
Ex. historical, SSP1-2.6, SSP5-8.5, etc.

**What environmental variable(s) do you need?**
For a full list of variables available, check the [ISIMIP data portal](https://data.isimip.org/search/tree/ISIMIP3b/InputData/climate/ocean/tree/ISIMIP3a/InputData/climate/ocean/)

**What is the time period of interest?**
Ex. I need data from January 1980 to December 2010.

**How do you need data to be summarised?**
ESM data is gridded and are available as monthly means. If you need data summarised in a different way, please provide details here. Ex. I need gridded yearly means, or I need monthly means weighted by area of grid cell (i.e., a single value for every month).

**We can provide extracted data in two file formats: csv and netCDF, which one do you prefer?**
