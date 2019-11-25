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
	data_city <- "CHI"
	
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
drop_rows <- function(df) {
	
	df %>%
		# Filters out "stale" requests. In Chicago, will filter out mostly outdated tobacco complaints.
		filter((updt_dt - req_dt) < years(3))
	
}

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
	print("Writing out the shapefiles of the entire dataset that you requested...")
	
	data %>%
		rename_data %>% 
		rectify_columns() %>% 
		drop_rows() %>% 
		st_write(paste0(project_dir, "/data/311/", data_city, "/", data_name,".shp"), delete_layer = TRUE)
	
	print("Shapefiles written!")
} else if (write_my_files == "yes") {
	print("Writing out the shapefiles of the entire dataset that you requested...")
	
	data %>%
		rename_data %>%
		rectify_columns() %>%
		drop_rows() %>%
		st_write(paste0(project_dir, "/data/311/", data_city, "/", data_name,".shp"), delete_layer = TRUE)
	
	print("Shapefiles written!")
}

data <-
	data %>% 
	rename_data() %>%
	rectify_columns() %>% 
	drop_rows()
	
data_write <-
	data %>% 
	st_drop_geometry() 

## For mapbox (testing)
# geojson_list(data, lat = lat, lon = long) %>% 
# 	geojson_write(file = "data/311/", data_name,"_mapbox.geojson")

if (!exists("write_my_files")) {
	print("Writing out tsv of entire dataset that you requested...")
	
	data_write %>% 
		write_tsv(paste0(project_dir, "/data/311/", data_city, "/", data_name,".tsv"))
	
	print("TSV written!")
} else if (write_my_files == "yes") {
	print("Writing out tsv of entire dataset that you requested...")
	
	data_write %>% 
		write_tsv(paste0(project_dir, "/data/311/", data_city, "/", data_name,".tsv"))
	
	print("TSV written!")
}

print(paste0("Preparing your ", data_city, " data for easy analysis..."))

# NOTE: This is a bit inefficient and we should consider holding off on joining all
# the descriptive data until here (We have been joining it the locating script).
data_descriptive <-
	data_write %>% 
	select(
		geoid,
		detail,
		contains("fip"),
		state,
		starts_with("pop"),
		starts_with("emp"),
		starts_with("ed"),
		starts_with("med")
	) %>% 
	distinct(geoid, .keep_all = TRUE) %>% 
	group_by(geoid) %>% 
	mutate(id = row_number()) %>% 
	left_join(
		data %>% 
			select(geoid, geometry) %>% 
			group_by(geoid) %>% 
			mutate(id = row_number()), 
		by = c("geoid", "id")
	) %>% 
	ungroup() %>% 
	select(-id)
	
data_calls <-
	data_write %>% 
	mutate(
		fix_min = ifelse(status == "closed", (updt_dt - req_dt) / 60, NA)
	) %>% 
	select(
		city,
		status,
		srvc_nm,
		address,
		req_dt,
		updt_dt,
		fix_min,
		geoid,
		topic,
		req_aim,
		illegal,
		adv
	)

print("You're all set!")

rm("write_my_files", "rename_data", "rectify_columns", "data", "data_write")
