#!/usr/bin/env python3

#Extracting ESM data using regional model boundaries.
#Author: Denisse Fierro Arcos
#Last updated: 2024-09-03
#This script needs to be run whenever there is an update of regional boundaries
#or ESM outputs.
#It is best run in NCI's Gadi, but file paths can be updated to work anywhere
#where GFDL outputs are stored

#Loading libraries
import xarray as xr
import zarr
import os
from glob import glob
import pandas as pd
import numpy as np
from datetime import datetime
import geopandas as gpd
import rioxarray
from dask.distributed import Client

#Starting a cluster
client = Client(threads_per_worker = 1)

# Loading gridded mask and regions shapefiles
# We will use these files to extract data for each FishMIP regional model. Note
# that the gridded mask **MUST** exactly match the ESM where we will extract 
# data.

#Loading FishMIP regional models shapefile
rmes = gpd.read_file(os.path.join('/g/data/vf71/shared_resources',\
                    'FishMIP_regional_models/FishMIP_regional_models.shp'))

#Loading FishMIP regional models gridded mask
path_mask_ras = os.path.join('/g/data/vf71/shared_resources/FishMIPMasks',\
                'merged_regional_fishmip',\
                'gfdl-mom6-cobalt2_areacello_15arcmin_fishMIP_regional_merged.nc')
mask_ras = xr.open_dataarray(path_mask_ras)
#Rechunking data to make it more manageable
mask_ras = mask_ras.chunk({'lat': 144, 'lon': 288})

# Setting up directories and files
#Base folder containing Earth System Model (ESM) data
base_dir = '/g/data/vf71/fishmip_inputs/ISIMIP3a/global_inputs/obsclim/025deg'
#Get a list of all files containing ESM outputs 
list_files = glob(os.path.join(base_dir, '*.nc'))

#Define (or create) folder for outputs
base_out = base_dir.replace('global', 'regional')
os.makedirs(base_out, exist_ok = True)


# Defining useful functions for data extraction
def open_ard_data(file_path, boolean_mask_ras):
    '''
    Open netCDF files in analysis ready data (ARD) format. That is apply chunks
    that make data analysis easier.
    
    Inputs:
    file_path (character): Full file path where netCDF file is stored.
    boolean_mask_ras (boolean data array): Data array to be used as initial mask
    to decrease the size of the original dataset. This mask makes no distinction
    between regional models, it simply identifies grid cells within regional 
    model boundaries with the value of 1.
    
    Outputs:
    da (data array): ARD data array containing data only for grid cells within
    regional model boundaries.
    '''

    #Getting chunks from gridded mask to apply it to model data array
    [lat_chunk] = np.unique(boolean_mask_ras.chunksizes['lat'])
    [lon_chunk] = np.unique(boolean_mask_ras.chunksizes['lon'])
    
    #Open data array
    da = xr.open_dataarray(file_path)
    
    #Checking if there is a fourth dimension in dataset, it is depth, but it is not
    #always called the same
    if len(da.dims) > 3:
        da = da.chunk({'time': 600, 'lev': 5, 'lat': lat_chunk, 'lon': lon_chunk})
        [depth_name] = [d for d in da.dims if d not in ['time', 'lat', 'lon']]
        #Changing depth dimension name
        da = da.rename({depth_name: 'depth_bin_m'})
    else:
        da = da.chunk({'time': 600, 'lat': lat_chunk, 'lon': lon_chunk})
    
    #Apply mask for all regions to decrease dataset size
    da = da.where(boolean_mask_ras == 1)
    
    #Add spatial information to dataset
    da.rio.set_spatial_dims(x_dim = 'lon', y_dim = 'lat', inplace = True)
    da.rio.write_crs('epsg:4326', inplace = True)
    
    #Change format of time dimension
    new_time = da.indexes['time'].to_datetimeindex()
    #Changing time in data array
    da['time'] = new_time

    return da

 
def mask_ard_data(ard_da, shp_mask, file_out):
    '''
    Open netCDF files in analysis ready data (ARD) format. That is apply chunks
    that make data analysis easier.
    
    Inputs:
    ard_da (data array): Analysis ready data (ARD) data array produced by the 
    function "open_ard_data"
    shp_mask (shapefile): Shapefile containing the boundaries of regional models
    file_out (character): Full file path where masked data should be stored.
    
    Outputs:
    No data is returned, but masked file will be stored in specified file path.
    '''

    #Clip data using regional shapefile
    da_mask = ard_da.rio.clip(shp_mask.geometry, shp_mask.crs, drop = True, 
                              all_touched = True)
    #Remove spatial information
    da_mask = da_mask.drop_vars('spatial_ref')
    da_mask.encoding = {}

    #Check file extension included in path to save data
    if file_out.endswith('zarr'):
        for i, c in enumerate(da_mask.chunks):
            if len(c) > 1 and len(set(c)) > 1:
                print(f'Rechunking {file_out}'.)
                print(f'Dimension "{da_mask.dims[i]}" has unequal chunks.')
                da_mask = da_mask.chunk({da_mask.dims[i]: '200MB'})
        da_mask.to_zarr(file_out, consolidated = True, mode = 'w')
    if file_out.endswith('parquet'):
        #Keep data array attributes to be recorded in final data frame
        da_attrs = ard_da.attrs
        da_attrs = pd.DataFrame([da_attrs])
        if 'time' in ard_da.coords:
            ind_wider = ['lat', 'lon', 'time', 'vals']
        else:
            ind_wider = ['lat', 'lon', 'vals']
        #Turn extracted data into data frame and remove rows with NA values
        df = da_mask.to_series().to_frame().reset_index().dropna()
        #Changing column name to standardise across variables
        df = df.rename(columns = {ard_da.name: 'vals'}).reset_index(drop = True)
        #Reorganise data
        df = df[ind_wider]
        #Include original dataset attributes
        df = pd.concat([df, da_attrs], axis = 1)
        #Saving data frame
        df.to_parquet(file_out)


# Extracting data from all model outputs for all FishMIP regional models
for f in list_files:
    #Open data array as ARD
    da = open_ard_data(f, mask_ras)
    da_clim = da.mean('time')

    #Create file name based on presence of depth dimension
    if 'depth_bin_m' in da.dims:
        base_file_out = os.path.basename(f).replace('.nc', '.zarr')
    else:
        base_file_out = os.path.basename(f).replace('.nc', '.parquet')
    #Adding output folder to create full file path
    down_file_out = os.path.join(base_out, base_file_out)
    map_file_out = os.path.join(clim_out, base_file_out)

    #Extract data for each region included in the regional mask
    for i in rmes.region:
        #Get polygon for each region
        mask = rmes[rmes.region == i]
        #Get name of region and clean it for use in output file
        reg_name = mask['region'].values[0].lower().replace(" ", "-").replace("'", "")
        #File name out - Replacing "global" for region name
        file_out = down_file_out.replace('global', reg_name)
        maps_file_out = map_file_out.replace('global', reg_name)
        #Extract data and save masked data - but only if file does not already exist
        if os.path.isdir(file_out) | os.path.isfile(file_out):
            continue
        mask_ard_data(da, mask, file_out)
        if os.path.isdir(maps_file_out) | os.path.isfile(maps_file_out):
            continue
        mask_ard_data(da_clim, mask, maps_file_out)
