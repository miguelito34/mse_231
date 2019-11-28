#!/usr/bin/env python
# coding: utf-8

# Imports
import xml.etree.ElementTree as ElementTree
import requests

URL_SUB_PAGE = "http://mobile311.sfgov.org/open311/v2/requests.xml?start_date=2007-02-19T00:00:00Z&end_date=2019-11-15T00:00:00Z&page="
PAGE_SIZE = 200
CITY_NAME = "San Francisco_CA"
FAILED_ATTEMPTS_LIMIT = 3

def get_requests_response_root(page):
    """Function to get a request by service_request_id"""
    url = URL_SUB_PAGE + str(page) + "&page_size=" + str(PAGE_SIZE)
    response = requests.get(url)
    try:
        root = ElementTree.fromstring(response.content)
        return(root)
    except ElementTree.ParseError:
        return(None)

def get_requests_data(vars_list, print_header=True):    
    # Print the header if requested
    if print_header:
        vars_dummy_dict = {i : "" for i in vars_list}
        vars_string = "\t".join(vars_dummy_dict.keys())
        print("city\t" + vars_string)
    page = 1
    failed_attempts = 0
    while True:
        # Make request
        print("Making request, page " + str(page))
        root = get_requests_response_root(page)
        if (root is None or root.find("request") is None):
            # Keep track of failed attempts, break once limit is hit
            failed_attempts += 1
            if (failed_attempts >= FAILED_ATTEMPTS_LIMIT):
                break
        else:
            # Reset failed attempts
            failed_attempts = 0
            for request in root.iter("request"):
                # Extract request data and store in dict
                request_data = {}
                for var in vars_list:
                    try:
                        data = request.find(var).text
                        # Ensure there are no tabs in the data
                        data.replace("\t","")
                        request_data[var] = data
                    except AttributeError:
                        # Handle missing/erroneous attributes by printing empty string
                        request_data[var] = ""
                    # Replace Python "None" values with empty string
                    if (request_data[var] is None):
                        request_data[var] = ""
                # If there is the minimum necessary data, print the observation
                if (request_data["service_name"] != "" and request_data["lat"] != "" and request_data["long"] != ""):                    
                    # Join the request data into a tab-separated string 
                    request_data_values_string = "\t".join(list(request_data.values()))
                    # Print with the associated city
                    print(CITY_NAME + "\t" + request_data_values_string)
        # Jump to the next page
        page += 1
                    
def main():
    vars_list = ["service_request_id","status","service_name","service_code","requested_datetime","updated_datetime","address","lat","long"]
    get_requests_data(vars_list)

if __name__== "__main__":
    main()