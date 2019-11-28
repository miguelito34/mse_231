#!/usr/bin/env python
# coding: utf-8

import requests
import sys

# Parameters
INDEX_LAT_Y = 8
INDEX_LON_X = 9


def get_geoid(lat, lon):
    """Function to get geoid and thus the tract number from a given call's coordinates"""
    url = f"https://geo.fcc.gov/api/census/block/find?latitude={lat}&longitude={lon}&format=json"
    response = requests.get(url).json()
    try:
        return (response['Block']['FIPS'][0:-4])
    except:
        return "NA"


# Finds geoid for all calls
for call in sys.stdin:
    call = call.strip()
    split_call = call.split('\t')
    
    # Checks if line is the header and if so, prints it along with the new geoid column
    if split_call[0] == "city":
        print(call + "\t" + "geoid")
        continue
    
    try:
        geoid = get_geoid(split_call[INDEX_LAT_Y], split_call[INDEX_LON_X])
    except:
        continue
    
    #If the call cannot be assigned to a census tract, throw it out
    if geoid != "NA":
        print(call + "\t" + geoid)