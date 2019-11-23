################################################################################
## Author: Michael Spencer, Andrew (Foster) Docherty, Jorge Nam Song,
##         Lauren Feitzinger, Andrea Banuet
## Project: MS&E 231 - 311 Calls
## Script Purpose: Clean and fully prep the 311 data prior to analysis
## Notes: 
################################################################################

if (!exists("project_dir")) {
	
	project_dir <- here::here()
	data_name <- "CHI_data_census"
	
	if (!require(sf)) install.packages("sf")
	library(sf)
	
	if (!require(tidyverse)) install.packages("tidyverse")
	library(tidyverse)
	
	if (!require(lubridate)) install.packages("lubridate")
	library(lubridate)
	
	if (!require(googlesheets4)) install.packages("googlesheets4")
	library(googlesheets4)
	
}

# Source data prep file to load data before cleaning here
source(paste0(project_dir, "/scripts/311/find_complaint_categories.R"))

# Drop any additional erroneous rows. Ideally this should be done in the earliest script possible.

# Dropping columns if unneccesary. Ideally this should be done in the earliest script possible.

# Renaming columns to seven characters or less for st_write formatting.
rename_data <- function(df) {
	
	df %>% 
		rename(
			srvc_nm = service_na,
			req_dt = requested_,
			updt_dt = updated_da
		)
	
}

# Changing column types
rectify_columns <- function(df) {
	
	df %>% 
		mutate(
			req_dt = 
				req_dt %>% 
				str_sub(start = 1L, end = -7L) %>% 
				ymd_hms(),
			updt_dt = 
				updt_dt %>% 
				str_sub(start = 1L, end = -7L) %>% 
				ymd_hms()
		)
	
}

# Write out if requested. Can be requested either by calling this script directly from the terminal
# or indicating such in the analysis scripts.
if (!exists("write_my_files")) {
	data %>%
		rename_data %>% 
		rectify_columns() %>% 
		st_write(paste0("data/311/", data_name,".shp"), delete_layer = TRUE)	
} else if (write_my_files == "yes") {
	data %>%
		rename_data %>%
		rectify_columns() %>%
		st_write(paste0("data/311/", data_name,".shp"), delete_layer = TRUE)	
}

data <-
	data %>% 
	rename_data() %>%
	rectify_columns() %>%
	st_drop_geometry()

## For mapbox (testing)
# geojson_list(data, lat = lat, lon = long) %>% 
# 	geojson_write(file = "data/311/", data_name,"_mapbox.geojson")

if (!exists("write_my_files")) {
	data %>% 
		write_tsv(paste0("data/311/", data_name,".tsv"))	
} else if (write_my_files == "yes") {
	data %>% 
		write_tsv(paste0("data/311/", data_name,".tsv"))
}

rm("write_my_files", "rename_data", "rectify_columns")
