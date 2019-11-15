#!/usr/bin/env python
# coding: utf-8

import requests
import sys

# Parameters
INDEX_LAT_Y = 8
INDEX_LON_X = 9


def get_geoid(lat, lon):
    """Function to get geoid and thus the tract number from a given call's coordinates"""
    url = f"https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={lon}&y={lat}&benchmark=4&vintage=415&layers=8&format=json"
    response = requests.get(url).json()
    try:
        return (response['result']['geographies']['Census Tracts'][0]['GEOID'])
    except:
        return "NA"


# Finds geoid for all calls
for call in sys.stdin:
    split_call = call.split('\t')
    
    # Checks if line is the header and if so, prints it along with the new geoid column
    if split_call[0] == "city":
        print(call + "\t" + "geoid")
        continue
        
    geoid = get_geoid(split_call[INDEX_LAT_Y], split_call[INDEX_LON_X])
    
    #If the call cannot be assigned to a census tract, throw it out
    if geoid != "NA":
        print(call + "\t" + geoid)