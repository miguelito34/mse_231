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
census_tracts = gpd.read_file(r'data/census/census_data_shapefiles.shp')[['geoid', 'geometry']]
calls = pd.read_csv(r'data_raw/311/sample_311_data.tsv', sep = "\t", index_col = 0)
calls = calls[calls.lat.notnull() & calls.long.notnull()]

# Creates a spatial dataframe of the calls and their lat/long before joining it with the census data
gdf = gpd.GeoDataFrame(calls, crs = {'init' :'epsg:4269'}, geometry = [Point(xy) for xy in zip(calls.long, calls.lat)])

located_311_data = sjoin(gdf, census_tracts, how='left').drop(['index_right', 'geometry'], axis = 1)

located_311_data.to_csv((PROJECT_PATH + '/data_raw/311/sample_311_data_geoid.tsv'), sep = "\t", index=False)