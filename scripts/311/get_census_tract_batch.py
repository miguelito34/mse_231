#!/usr/bin/env python
# coding: utf-8

import geopandas as gpd
from geopandas.tools import sjoin
import pandas as pd
from shapely.geometry import Point
import os
import rtree
import sys

# Parameters
PROJECT_PATH = os.getcwd()

# Loads relevant census and 311 call data

#census_tracts = gpd.read_file(r'data/census/census_data_shapefiles.shp')[['geoid', 'geometry']] # Use this to drop columns
census_tracts = gpd.read_file(r'data/census/census_data_shapefiles.shp') # Use this to keep all columns, i.e. if doing things entirely in memory

calls = pd.read_csv((r'data_raw/311/unjoined/' + sys.argv[1] + '_data.tsv'), sep = "\t")
calls = (calls[calls.lat.notnull() & calls.long.notnull()]
         .drop_duplicates()
         .drop(['service_request_id', 'service_code'], axis = 1)
        )

# Creates a spatial dataframe of the calls and their lat/long before joining it with the census data
gdf = gpd.GeoDataFrame(calls, crs = {'init' :'epsg:4269'}, geometry = [Point(xy) for xy in zip(calls.long, calls.lat)])
gdf = gdf[gdf.geometry.type == "Point"]
gdf = gdf[0:1]
located_311_data = sjoin(gdf, census_tracts, how = 'left')

# I have positively no idea why, but running this again seems to be the only way to make this work, major debugging needed, might try in R.
gdf = gpd.GeoDataFrame(calls, crs = {'init' :'epsg:4269'}, geometry = [Point(xy) for xy in zip(calls.long, calls.lat)])
gdf = gdf[gdf.geometry.type == "Point"]
located_311_data = (sjoin(gdf, census_tracts, how = 'left')
                    .drop(['index_right', 'geometry'], axis = 1)
                    .merge(census_tracts[['geoid', 'geometry']], on = "geoid")
                   )

located_311_data.to_file((PROJECT_PATH + '/data_raw/311/joined/' + sys.argv[1] + '_data_census.shp'))