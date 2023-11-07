# FishMIP_regional models
The Fisheries and Marine Ecosystem Model Intercomparison Project ([Fish-MIP](https://fish-mip.github.io/)) aims to improve our understanding of the long-term impacts of climate change on fisheries and marine ecosystems, so we can improve future projections, which in turn can help inform policy.  
  
Our include includes several global and regional ecosystem models. In this repository, we create a single shapefile containing all regional model contributions to Fish-MIP. We can use this file to create [maps](Outputs/FishMIP_regional_models.pdf) and to extract forcing data from Earth System Models (ESMs) for regional ecosystem modellers.  
  
If you are interested in submitting your regional model to the Fish-MIP group, please contact our **Regional Model Coordinators**. You can find their contact details in our [website](https://fish-mip.github.io/).  
  
Due to the large size of files, we are not able to share all individual model boundaries, but we are sharing a compressed (`zip`) folder containing the shapefile with all Fish-MIP regions in the [Outputs folder](Outputs/FishMIP_regional_models.zip). Alternatively, this shapefile is also available from the [FishMIP THREDDS server](http://portal.sf.utas.edu.au/thredds/catalog/gem/fishmip/FishMIP_regions/catalog.html).  
  
[Map of Fish-MIP regional models](Outputs/FishMIP_regional_models.pdf).  

## Table of contents
- [Merging regional shapefiles into a single file](Scripts/01_Merging_Regional_Shapefiles.md): This `R` notebook shows how we created a single shapefile containing all regional model boundaries.  
- [Mapping regional shapefiles](Scripts/02_Mapping_Regional_Models.md): This `R` notebook shows how we created a simple map of Fish-MIP regional models, and how to create a map with insets.  
- [Creating two dimensional raster masks](Scripts/03a_Regional_Models_2DMasks.md): This `R` notebook shows how to create a raster mask that can be used to extract data from ESM outputs.  
- [Outputs folder](Outputs/): Contains files produced by code contained in the [Scripts folder](Scripts/). This is where you will find the final Fish-MIP regional models shapefile.  
- [ESM_Sample_Data.zip](ESM_Sample_Data.zip): Compressed folder containing a sanples of all model grids used within the Fish-MIP group.  
  
## Have questions or suggestions?
Feel free to create an [Issue](https://github.com/Fish-MIP/FishMIP_regions/issues) or [email us](mailto:fishmip.coordinators@gmail.com).  
  