#!/usr/bin/env python
# coding: utf-8

import geopandas as gpd
from geopandas.tools import sjoin
import pandas as pd
from shapely.geometry import Point
import os
import rtree

# Parameters
PROJECT_PATH = os.getcwd()

# Loads relevant census and 311 call data


#census_tracts = gpd.read_file(r'data/census/census_data_shapefiles.shp')[['geoid', 'geometry']] # Use this to drop columns
census_tracts = gpd.read_file(r'data/census/census_data_shapefiles.shp') # Use this to keep all columns, i.e. if doing things entirely in memory


calls = pd.read_csv(r'data_raw/311/unjoined/sample_311_data_300k_BOS_CHI_SFO.tsv', sep = "\t", index_col = 0)
calls = calls[calls.lat.notnull() & calls.long.notnull()]

# Creates a spatial dataframe of the calls and their lat/long before joining it with the census data
gdf = gpd.GeoDataFrame(calls, crs = {'init' :'epsg:4269'}, geometry = [Point(xy) for xy in zip(calls.long, calls.lat)])
gdf = gdf[gdf.geometry.type == "Point"]
gdf = gdf[0:1]
located_311_data = sjoin(gdf, census_tracts, how = 'left').drop(['index_right', 'geometry'], axis = 1)

# I have positively no idea why, but running this again seems to be the only way to make this work, major debugging needed, might try in R.
gdf = gpd.GeoDataFrame(calls, crs = {'init' :'epsg:4269'}, geometry = [Point(xy) for xy in zip(calls.long, calls.lat)])
gdf = gdf[gdf.geometry.type == "Point"]
located_311_data = sjoin(gdf, census_tracts, how = 'left')

located_311_data.to_file((PROJECT_PATH + '/data_raw/311/joined/sample_311_data_300k_BOS_CHI_SFO_census.shp'))

located_311_data = located_311_data.drop(['index_right', 'geometry'], axis = 1)
located_311_data.to_csv((PROJECT_PATH + '/data_raw/311/joined/sample_311_data_300k_BOS_CHI_SFO_census.tsv'), sep = "\t", index = False)