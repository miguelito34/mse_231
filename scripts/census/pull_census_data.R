################################################################################
## Author: Michael Spencer, Andrew (Foster) Docherty, Jorge Nam Song,
##         Lauren Feitzinger, Andrea Banuet
## Project: MS&E 231 - 311 Calls
## Script Purpose: Gather census data for relevant block groups in analyzed cities
## Notes: Uses tidycensus package to gather relevant tables on ethnicity/race,
##        education, median household income, employment status
################################################################################

## Setup

### Libraries
if (!require(tidycensus)) install.packages("tidycensus")
library(tidycensus)

if (!require(sf)) install.packages("sf")
library(sf)

if (!require(tidyverse)) install.packages("tidyverse")
library(tidyverse)

### Parameters
source("scripts/census/load_census_query.R")
source("credentials.R")
census_api_key(my_census_api_key)

#===============================================================================

### Functions
# This function takes the raw tidycensus data and tranforms into our desirable format.
transform_census_data <- function(data, st, cty) {
	
	data %>% 
		group_by(NAME) %>%
		spread(key = variable, value = estimate) %>%
		ungroup() %>% 
		transmute(
			geoid    = GEOID,
			detail   = NAME,
			st_fip   = str_sub(geoid, 1L, 2L),
			cty_fip  = str_sub(geoid, 3L, 5L),
			trt_fip  = str_sub(geoid, 6L, 11L),
			state    = st,
			county   = cty,
			geometry = st_cast(geometry, "MULTIPOLYGON"),
			pop_tot  = pop_total,
			pop_wht  = pop_num_white/pop_total,
			pop_blk  = pop_num_black/pop_total,
			pop_his  = pop_num_hisp/pop_total,
			pop_asi  = pop_num_asian/pop_total,
			pop_two  = pop_two_plus/pop_total,
			pop_oth  = pop_num_other/pop_total,
			pop_nat  = pop_num_native/pop_total,
			pop_isl  = pop_num_islander/pop_total,
			pop_nw   = 1 - pop_wht,
			emp_une  = emp_unemp/emp_total,
			emp_emp  = 1 - emp_une,
			ed_grad  = (ed_prof + ed_phd + ed_ms)/ed_total,
			ed_bs    = ed_bs/ed_total,
			ed_as    = ed_as/ed_total,
			ed_hs    = (ed_hs_college_nf + ed_hs_ged + ed_hs_hs + ed_hs_some_college)/ed_total,
			ed_l_hs  = 1 - (ed_grad + ed_bs + ed_as + ed_hs),
			med_inc  = med_income
		)
}

### Get Data
data_census <- tibble() %>% data.table::as.data.table()

for (st in table_geos$state) {
	
	counties <- table_geos %>% filter(state == st) %>% pull(counties) %>% unlist()
	
	for (cty in counties) {
		
		this_county <-
			get_acs(
				geography = "tract",
				variables = table_census_vars,
				state = st,
				county = cty,
				year = 2015,
				geometry = TRUE
			) %>% 
			select(-moe) %>% 
			transform_census_data(st, cty) %>%
			data.table::as.data.table()
			
		# Appends data for all counties together into single table
		data_census <- data.table::rbindlist(list(data_census, this_county))

	}
}

data_census <- data_census %>% st_sf()

### Write Data
data_census %>%
	st_write("./data/census/census_data_shapefiles.shp", delete_dsn = TRUE, delete_layer = TRUE)

data_census %>%
	st_drop_geometry() %>%
	write_tsv(path = "./data/census/census_data.tsv.gz")
