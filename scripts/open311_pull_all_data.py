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
## Domains for available Open311 GeoReport v2 city APIs
DOMAINS = {
    "Bloomington_IN": "bloomington.in.gov/crm",
    "Boston_MA": "311.boston.gov",
    "Brookline, MA": "spot.brooklinema.gov",
    "Chicago, IL": "311api.cityofchicago.org",
    "Peoria_IL": "ureport.peoriagov.org/crm",
    "San Francisco_CA": "mobile311.sfgov.org"
}

def get_service_names_response_root(domain):
    """Function to get the services names available for a given domain"""
    response = requests.get(f"https://{domain}/open311/v2/services.xml")
    root = ElementTree.fromstring(response.content)
    return(root)

def get_requests_response_root(domain, start_datetime_string, end_datetime_string, status):
    """Function to get the requests for a given domain, start/end datetime, and status"""
    response = requests.get(f"http://{domain}/open311/v2/requests.xml?start_date={start_datetime_string}&end_date={end_datetime_string}&status={status}")
    root = ElementTree.fromstring(response.content)
    return(root)

def datetime_to_string(datetime_obj):
    """Function to convert a datetime into a request-compatible string"""
    return(f"{datetime_obj.date()}T{datetime_obj.time()}Z")

def get_requests_data(vars_list, status, num_90day_iters=1, print_header=True):    
    # Get current datetime and datetime for start of today
    now = dt.datetime.now()
    today = now - dt.timedelta(hours = now.hour, minutes = now.minute, seconds = now.second, microseconds = now.microsecond)

    if print_header:
        vars_dummy_dict = {i : "" for i in vars_list}
        vars_string = "\t".join(vars_dummy_dict.keys())
        print(f"city\t{vars_string}")

    for city, domain_value in DOMAINS.items():
        start_datetime = today
        for i in range(num_90day_iters):
            end_datetime = start_datetime
            start_datetime = end_datetime - dt.timedelta(days = OPEN311_RANGE)
            root = get_requests_response_root(domain_value, 
                                              datetime_to_string(start_datetime), 
                                              datetime_to_string(end_datetime),
                                              status)
            # print(ElementTree.tostring(root, encoding='utf8').decode('utf8'))
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
                request_data_values_string = "\t".join(list(request_data.values()))
                print(f"{city}\t{request_data_values_string}")

def main():
    vars_list = ["service_request_id","status","status_notes","service_name","service_code","requested_datetime","updated_datetime","address","lat","long"]
    get_requests_data(vars_list, "open")
    get_requests_data(vars_list, "closed", print_header=False)

if __name__== "__main__":
    main()





