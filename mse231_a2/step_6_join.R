################################################################################
## Project: MS&E Assignment 2
## Script purpose: Join EMR output trip data with precipitation data
## Date: 2019-10-25
## Author: Michael Spencer, Foster Docherty, Jorge Nam Song
################################################################################

## Setup

### Load Libraries
if (!require(tidyverse)) install.packages("tidyverse")
library(tidyverse)
if (!require(lubridate)) install.packages("lubridate")
library(lubridate)

### Parameters
path_trip_data <- "agg_trip_data.csv"
path_precipitation_data <- "https://5harad.com/data/nyctaxi/nyc_precipitation.csv"

### Load Data
data_trips <- 
	path_trip_data %>% 
	read_csv() %>% 
	mutate(
		date = .$date %>% mdy() %>% as.character(),
		hour = .$hour %>% as.integer()
	) %>% 
	filter(earnings > 0) # Had one day where earnings were negative, so we filtered it out

data_precipitation <- 
	path_precipitation_data %>% 
	read_csv() %>% 
	select(
		datetime = "DATE",
		precip = "HPCP"
	) %>% 
	transmute(
		date = ymd_hms(datetime) %>% date() %>% as.character(),
		hour = ymd_hms(datetime) %>% hour() %>% as.integer(),
		precip
	)

## Data Transformation
data <-
	data_trips %>% 
	left_join(data_precipitation, by = c("date", "hour")) %>% 
	mutate(precip = ifelse(is.na(precip), 0, precip)) %>%
	arrange(date, hour) %>% 
	write_tsv(path = "nyc_taxi_rain.tsv") 
	
rm(data_precipitation, data_trips, path_precipitation_data, path_trip_data, data)
