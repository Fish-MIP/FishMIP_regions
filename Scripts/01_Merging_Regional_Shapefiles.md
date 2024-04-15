Merging FishMIP Regional Shapefiles
================
Denisse Fierro Arcos
2023-10-31

- <a href="#introduction" id="toc-introduction">Introduction</a>
- <a href="#loading-r-libraries" id="toc-loading-r-libraries">Loading R
  libraries</a>
- <a href="#loading-regional-shapefiles"
  id="toc-loading-regional-shapefiles">Loading regional shapefiles</a>
  - <a href="#getting-list-of-directories"
    id="toc-getting-list-of-directories">Getting list of directories</a>
  - <a href="#getting-list-of-lme-names-from-directory-paths"
    id="toc-getting-list-of-lme-names-from-directory-paths">Getting list of
    LME names from directory paths</a>
  - <a href="#loading-regions" id="toc-loading-regions">Loading regions</a>
  - <a href="#plotting-merged-regions-in-a-map"
    id="toc-plotting-merged-regions-in-a-map">Plotting merged regions in a
    map</a>

# Introduction

In this notebook, we will use shapefiles submitted by all FishMIP
regional modelers to create a single file that can then be used to
create maps or masks to extract Earth System Models (ESMs) outputs.

# Loading R libraries

``` r
#Data manipulation
library(dplyr)
library(stringr)
library(purrr)
library(tidyr)
#Spatial data
library(sf)
#Plotting data
library(ggplot2)
#Base maps
library(rnaturalearth)
```

# Loading regional shapefiles

Due to the total size of regional shapefiles, it is not possible to
share them in this repository. However, the merged file is available in
the FishMIP THREDDS server. Click
[here](http://portal.sf.utas.edu.au/thredds/catalog/gem/fishmip/FishMIP_regions/catalog.html)
to access this file.

If you need access to regional shapefiles, please [email
us](mailto:fishmip.coordinators@gmail.com).

## Getting list of directories

The name of the folders containing regional shapefiles contain the
ecosystem models developed for that particular region. We will use this
information to create two new columns in the final FishMIP regional
models shapefile.

``` r
#Getting name of folders containing regional models
reg <- list.dirs("../Shapefiles_Regions/", recursive = F, full.names = F)

#Creating a table with ecosystem models available per region
reg_info <- str_split(reg, "_", simplify = T) |>
  data.frame() |> 
  #Renaming columns
  rename(region = X1, model_all = X2) |> 
  #Replace "-" with a space in the region name
  mutate(region = str_replace_all(region, "-", " "),
         #Replace "-" with a comma in the ecosystem models column
         models = str_replace_all(model_all, "-", ", ")) |> 
  #Counting the number of ecosystem models available per region
  separate_longer_delim(model_all, delim = "-") |> 
  group_by(region, models) |> 
  count(name = "number_models")
```

## Getting list of LME names from directory paths

``` r
#Getting a list of shapefiles in the folder containing the regional model boundaries
region_paths <- list.files("../Shapefiles_Regions", pattern = ".shp$", recursive = T, full.names = T)
#Remove any shapefiles included in "Support Info" folders
region_paths <- region_paths[!str_detect(region_paths, "SupportInfo")]
```

## Loading regions

As of December 2023, there are 33 regional FishMIP models. We will use
the boundaries for all these regions to create a single shapefile that
includes all FishMIP regional models. Having a single file is useful to
create maps showing all regional models easily. This file can also be
used to create masks and extract data from Earth System Models (ESMs).

The regional shapefiles used here have been previously standardised, so
they are easier to merge. All shapefiles now have the following
characteristics:  
- Longitudes range from $-180^{\circ}$ to $180^{\circ}$  
- If a shapefile crosses the international date line, it is split in
two  
- Any internal boundaries were removed  
- All shapefiles have two columns only: `region` and `geometry`  
- The coordinate reference system (CRS) was set to WGS84
([EPSG:4326](https://epsg.io/4326))

``` r
#Loading all files into a list and creating a single shapefile with all regions
regions <- region_paths |> 
  map(read_sf) |> 
  bind_rows() |> 
  #Cleaning up names - Replace "_" for spaces " "
  mutate(region = str_replace_all(region, "_", " ")) |> 
  #Adding model names and number of ecosystem models available per region
  left_join(reg_info, by = "region") |> 
  #Moving geometry to the end
  relocate(geometry, .after = number_models)
```

## Plotting merged regions in a map

Before we save the merged shapefile, we will create a simple map to
check that all regions are showing correctly. We will use a world
basemap from the `rnaturalearth` package.

``` r
#Loading basemap
world <- ne_countries(returnclass = "sf")

#Plotting regions and map of the world
ggplot()+
  geom_sf(data = world)+
  geom_sf(data = regions, aes(fill = region, alpha = 0.5))+
  theme_bw()+
  theme(legend.position = "bottom", legend.title = element_blank())+
  guides(fill = guide_legend(ncol = 4))
```

![](01_Merging_Regional_Shapefiles_files/figure-gfm/map-1.png)<!-- -->

The merged shapefile includes 33 different regions, which matches the
number of regional FishMIP models. We can now save this merged file.

``` r
#Location of folder for outputs
out_folder <- "../Outputs/FishMIP_regional_models"
#If folder does not exist, create one
if(!dir.exists(out_folder)){
  dir.create(out_folder, recursive = T)}

regions |> 
  write_sf(file.path(out_folder, "FishMIP_regional_models.shp"), append = F)
```

Remember, the final shapefile is also available in the [FishMIP THREDDS
server](http://portal.sf.utas.edu.au/thredds/catalog/gem/fishmip/FishMIP_regions/catalog.html).
