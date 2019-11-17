#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ElementTree
import requests
import pandas as pd
import os

PROJECT_PATH = os.getcwd()

DOMAINS = {
    "Bloomington_IN": "bloomington.in.gov/crm",
    "Boston_MA": "311.boston.gov",
    "Brookline, MA": "spot.brooklinema.gov",
    "Chicago, IL": "311api.cityofchicago.org",
    "Peoria_IL": "ureport.peoriagov.org/crm",
    "San Francisco_CA": "mobile311.sfgov.org"
}

URL_START = "http://"
URL_END = "/open311/v2/services.xml"

def main():
    dummy_list = []
    df_service_names_all = pd.DataFrame(dummy_list, columns=["dummy"])

    for key in DOMAINS:
        response = requests.get(URL_START + DOMAINS[key] + URL_END)
        root = ElementTree.fromstring(response.content)
        service_names = []
        for service_name in root.iter("service_name"):
            service_names.append(service_name.text)
        df_service_names = pd.DataFrame(service_names, columns=[key])
        df_service_names_all = pd.concat([df_service_names_all, df_service_names], axis=1)

    df_service_names_all = df_service_names_all.drop(['dummy'], axis=1)
    df_service_names_all.to_csv((PROJECT_PATH + '/data/311/service_names.csv'), index=False)

if __name__== "__main__":
    main()
