#!/usr/bin/env python
import xml.etree.ElementTree as ElementTree
import requests
import pandas as pd

# GeoReport v2 API endpoinits
response_SF = requests.get('http://mobile311.sfgov.org/open311/v2/services.xml')
response_Chicago = requests.get('http://311api.cityofchicago.org/open311/v2/services.xml')
response_Boston = requests.get('https://311.boston.gov/open311/v2/services.xml')

# XML roots
root_SF = ElementTree.fromstring(response_SF.content)
root_Chicago = ElementTree.fromstring(response_Chicago.content)
root_Boston = ElementTree.fromstring(response_Boston.content)

# Collect service names in Pandas DataFrames
service_names_SF = []
for service_name in root_SF.iter('service_name'):
    service_names_SF.append(service_name.text)
df_service_names_SF = pd.DataFrame(service_names_SF, columns=["SF"])

service_names_Chicago = []
for service_name in root_Chicago.iter('service_name'):
    service_names_Chicago.append(service_name.text)
df_service_names_Chicago = pd.DataFrame(service_names_Chicago, columns=["Chicago"])

service_names_Boston = []
for service_name in root_Boston.iter('service_name'):
    service_names_Boston.append(service_name.text)
df_service_names_Boston = pd.DataFrame(service_names_Boston, columns=["Boston"])

# Concatenate the DataFrames
df_service_names = pd.concat([df_service_names_SF, df_service_names_Chicago], axis=1) 
df_service_names = pd.concat([df_service_names, df_service_names_Boston], axis=1) 

# Save to .csv
df_service_names.to_csv('service_names.csv', index=False)



