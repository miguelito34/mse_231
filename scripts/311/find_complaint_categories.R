################################################################################
## Author: Michael Spencer, Andrew (Foster) Docherty, Jorge Nam Song,
##         Lauren Feitzinger, Andrea Banuet
## Project: MS&E 231 - 311 Calls
## Script Purpose: Match the 311 call data to a given complaint category
## Notes: Complaints are currently categorized as human or non-human though
##        further categorization may be needed.
################################################################################

## Setup

### Libraries
if (!require(sf)) install.packages("sf")
library(sf)

if (!require(tidyverse)) install.packages("tidyverse")
library(tidyverse)

### Parameters
path_categories <- "data/311/complaint_categorization.csv" # Ensure you have the latest table from Google Sheets.
path_data_shapefiles <- "data_raw/311/joined/sample_311_data_300k_BOS_CHI_SFO_census.shp"

### Load Data
data_categories <- path_categories %>% read_csv()
data_shapefiles <- 
    path_data_shapefiles %>% 
    st_read() %>% 
    mutate(city = str_extract(city, pattern = ".+(?=[,_])"))

#===============================================================================

## Join and Write Data
data_write <- 
    data_shapefiles %>% 
    left_join(data_categories, by = c("city", "service_na" = "req_name"))

data_write %>%
    st_write("data/311/sample_311_data_300k_BOS_CHI_SFO_clean.shp")

data_shapefiles %>% 
    left_join(data_categories, by = c("city", "service_na" = "req_name")) %>%
    select(-geometry) %>%
    write_tsv("data/311/sample_311_data_300k_BOS_CHI_SFO_clean.tsv")