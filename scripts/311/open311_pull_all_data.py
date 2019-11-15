#!/usr/bin/env python
# coding: utf-8

# Imports
import xml.etree.ElementTree as ElementTree
import requests
import pandas as pd
import datetime as dt
import csv

## Domains for available Open311 GeoReport v2 city APIs
DOMAINS = {
    "Bloomington_IN": "bloomington.in.gov/crm",
    "Boston_MA": "311.boston.gov",
    "Brookline, MA": "spot.brooklinema.gov",
    "Chicago, IL": "311api.cityofchicago.org",
    "Peoria_IL": "ureport.peoriagov.org/crm",
    "San Francisco_CA": "mobile311.sfgov.org"
}

SERVICE_REQUEST_ID_END = {
    "Bloomington_IN": "170962",
    "Boston_MA": "101003103001",
    "Brookline, MA": "22925",
    "Chicago, IL": "02950001",
    "Peoria_IL": "27365",
    "San Francisco_CA": "11687000"
}

# Cities that support comma-delimeted IDs
COMMA = {
    "Brookline, MA": "100"
}

COMMA_AND_PAGE_SIZE = {
    "Boston_MA": "250",
    "Chicago, IL": "500",
    "San Francisco_CA": "500"
}

def get_requests_response_root(domain, service_request_id):
    """Function to get a request by service_request_id"""
    response = requests.get(f"http://{domain}/open311/v2/requests.xml?service_request_id={service_request_id}")
    root = ElementTree.fromstring(response.content)
    return(root)

def get_requests_response_root_page_size(domain, service_request_id, page_size):
    """Function to get a request by service_request_id"""
    response = requests.get(f"http://{domain}/open311/v2/requests.xml?page_size={page_size},service_request_id={service_request_id}")
    root = ElementTree.fromstring(response.content)
    return(root)

def datetime_to_string(datetime_obj):
    """Function to convert a datetime into a request-compatible string"""
    return(f"{datetime_obj.date()}T{datetime_obj.time()}Z")

def get_requests_data(vars_list, print_header=True):    
    # Get current datetime and datetime for start of today
    now = dt.datetime.now()
    today = now - dt.timedelta(hours = now.hour, minutes = now.minute, seconds = now.second, microseconds = now.microsecond)

    # Print the header if requested
    if print_header:
        vars_dummy_dict = {i : "" for i in vars_list}
        vars_string = "\t".join(vars_dummy_dict.keys())
        print(f"city\t{vars_string}")

    min_data_points_per_city = 2
    # Iterate over cities
    for city, domain_value in DOMAINS.items():
        # Start with the id specified for each city
        curr_service_request_id = SERVICE_REQUEST_ID_END[city]
        # Keep track of how many data points we have printed for this city
        total_data_count = 0
        while (total_data_count < min_data_points_per_city):
            # If the city supports comma-delimeted IDs and page_size, ask for multiple with max page_size
            # Elif the city supports comma-delimeted IDs, ask for multiple. 
            # Else, request IDs one-by-one
            if (city in COMMA_AND_PAGE_SIZE):
                curr_num = int(curr_service_request_id)
                num_minus_page_size = curr_num - int(COMMA_AND_PAGE_SIZE[city])
                service_request_id_list = [str(i) for i in range(num_minus_page_size + 1, curr_num + 1)]
                service_request_id_list_string = ",".join(service_request_id_list)

                # Make the GET request for the data and receive the root of the XML-parsed ElementTree
                #print(f"Making request: city={city}, starting with curr_service_request_id={curr_service_request_id}, page_size={COMMA_AND_PAGE_SIZE[city]}") # DEBUG
                root = get_requests_response_root_page_size(domain_value, 
                                                  service_request_id_list_string,
                                                  COMMA_AND_PAGE_SIZE[city])
                # Try to get a 311 request from the id
                request_test = root.find("request")
                if request_test is not None:
                    for request in root.iter("request"):
                        # Extract request data and store in dict
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

                        if (request_data["service_name"] != "" and request_data["lat"] != "" and request_data["long"] != ""):                    
                            # Join the request data into a tab-separated string 
                            request_data_values_string = "\t".join(list(request_data.values()))

                            # Print with the associated city
                            print(f"{city}\t{request_data_values_string}")

                            # Increment data_count for this data point
                            total_data_count += 1
                # Decrement id for requesting prev id 
                curr_service_request_id = str(num_minus_page_size)
            elif(city in COMMA):
                curr_num = int(curr_service_request_id)
                num_minus_page_size = curr_num - int(COMMA[city])
                service_request_id_list = [str(i) for i in range(num_minus_page_size + 1, curr_num + 1)]
                service_request_id_list_string = ",".join(service_request_id_list)

                # Make the GET request for the data and receive the root of the XML-parsed ElementTree
                #print(f"Making request: city={city}, starting with curr_service_request_id={curr_service_request_id}") # DEBUG
                root = get_requests_response_root(domain_value, 
                                                  service_request_id_list_string)
                # Try to get a 311 request from the id
                request_test = root.find("request")
                if request_test is not None:
                    for request in root.iter("request"):
                        # Extract request data and store in dict
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

                        if (request_data["service_name"] != "" and request_data["lat"] != "" and request_data["long"] != ""):                    
                            # Join the request data into a tab-separated string 
                            request_data_values_string = "\t".join(list(request_data.values()))

                            # Print with the associated city
                            print(f"{city}\t{request_data_values_string}")

                            # Increment data_count for this data point
                            total_data_count += 1
                # Decrement id for requesting prev id 
                curr_service_request_id = str(num_minus_page_size)
            else:
                # Make the GET request for the data and receive the root of the XML-parsed ElementTree
                #print(f"Making request: city={city}, curr_service_request_id={curr_service_request_id}") # DEBUG
                root = get_requests_response_root(domain_value, 
                                                  curr_service_request_id)

                # Try to get a 311 request from the id
                request = root.find("request")
                if request is not None:
                    # Extract request data and store in dict
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

                    # Join the request data into a tab-separated string 
                    request_data_values_string = "\t".join(list(request_data.values()))

                    # Print with the associated city
                    print(f"{city}\t{request_data_values_string}")

                    # Increment data_count for this data point
                    total_data_count += 1

                # Decrement id for requesting prev id 
                curr_service_request_id = str(int(curr_service_request_id) - 1)
                    
def main():
    vars_list = ["service_request_id","status","service_name","service_code","requested_datetime","updated_datetime","address","lat","long"]
    get_requests_data(vars_list)

if __name__== "__main__":
    main()





