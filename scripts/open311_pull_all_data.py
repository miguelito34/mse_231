#!/usr/bin/env python
# coding: utf-8

# Imports
import xml.etree.ElementTree as ElementTree
import requests
import pandas as pd
import datetime as dt
import csv

# Constants
OPEN311_RANGE = 90 # Open311 can only take 90 requests at a time
#DATA_LIMIT_ADJUSTMENT = dt.timedelta(minutes = 10)

## Domains for available Open311 GeoReport v2 city APIs
DOMAINS = {
    #"Bloomington_IN": "bloomington.in.gov/crm",
    "Boston_MA": "311.boston.gov",
    "Brookline, MA": "spot.brooklinema.gov",
    "Chicago, IL": "311api.cityofchicago.org",
    "Peoria_IL": "ureport.peoriagov.org/crm",
    "San Francisco_CA": "mobile311.sfgov.org"
}

DATA_LIMITS = {
    #"Bloomington_IN": 1000,
    "Boston_MA": 50,
    "Brookline, MA": 100,
    "Chicago, IL": 50,
    "Peoria_IL": 1000,
    "San Francisco_CA": 50
}

def get_requests_response_root(domain, start_datetime_string, end_datetime_string, status):
    """Function to get the requests for a given domain, start/end datetime, and status"""
    response = requests.get(f"http://{domain}/open311/v2/requests.xml?start_date={start_datetime_string}&end_date={end_datetime_string}&status={status}")
    root = ElementTree.fromstring(response.content)
    return(root)

def datetime_to_string(datetime_obj):
    """Function to convert a datetime into a request-compatible string"""
    return(f"{datetime_obj.date()}T{datetime_obj.time()}Z")

def get_requests_data(vars_list, status, start_datetime, num_90day_iters=1, print_header=True):    
    # Get current datetime and datetime for start of today
    now = dt.datetime.now()
    today = now - dt.timedelta(hours = now.hour, minutes = now.minute, seconds = now.second, microseconds = now.microsecond)

    # Print the header if requested
    if print_header:
        vars_dummy_dict = {i : "" for i in vars_list}
        vars_string = "\t".join(vars_dummy_dict.keys())
        print(f"city\t{vars_string}")

    # Iterate over cities
    for city, domain_value in DOMAINS.items():
        # Reset end datetime to today
        end_datetime = today - dt.timedelta(days = 1)
        # Loop until we have covered the entire requested datetime range
        while (end_datetime.date() > start_datetime.date()):

            # Make the GET request for the data and receive the root of the XML-parsed ElementTree
            print(f"Making request: city={city}, start={start_datetime}, end={end_datetime}, status={status}") # DEBUG
            root = get_requests_response_root(domain_value, 
                                              datetime_to_string(start_datetime), 
                                              datetime_to_string(end_datetime),
                                              status)
            # Counter to keep track of how many data points we have already printed
            data_count = 0
            # Chicago fix
            requested_datetime_list = []
            # Iterate over the 311 requests we received
            for request in root.iter('request'):
                request_data = {}

                for var in vars_list:
                    try:
                        data = request.find(var).text
                        data.replace("\t","")
                        request_data[var] = data
                    except AttributeError:
                        request_data[var] = ""
                    if (request_data[var] is None):
                        request_data[var] = ""

                # Chicago fix
                if (city == "Chicago, IL"):
                    requested_datetime_list.append(request_data["requested_datetime"])

                # Used to ensure that we have a valid end datetime to reset to
                if ("updated_datetime" in request_data):
                    end_datetime = dt.datetime.strptime(request_data["updated_datetime"][:19], "%Y-%m-%dT%H:%M:%S")
                    # print(f"current_end_datetime={current_end_datetime}") # DEBUG

                # Join the output variables into a tab-separated string 
                request_data_values_string = "\t".join(list(request_data.values()))
                # Print with the associated city
                print(f"{city}\t{request_data_values_string}")

                # Increment the data count for this data point
                data_count += 1

                # If we hit or exceeded or data points limit for that city, make a new data request the latest datetime.
                if (data_count >= DATA_LIMITS[city]):
                    print(f"Hit limt. data_count={data_count}, data_limit={DATA_LIMITS[city]}") # DEBUG
                    break

            # For Chicago, store and sort the series of requests by requested_datetime, 
            # using the min datetime as the new end_datetime 
            if (city == "Chicago, IL"):
                requested_datetime_list.sort()
                end_datetime = dt.datetime.strptime(requested_datetime_list[0][:19], "%Y-%m-%dT%H:%M:%S")
                    
def main():
    vars_list = ["service_request_id","status","status_notes","service_name","service_code","requested_datetime","updated_datetime","address","lat","long"]
    start_datetime = dt.datetime(2019, 11, 1, 0, 0, 0)
    get_requests_data(vars_list, "closed", start_datetime)
    #get_requests_data(vars_list, "closed", start_datetime, print_header=False)

if __name__== "__main__":
    main()





