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
# if (!require(raster)) install.packages("raster")
# library(raster)

if (!require(tidyverse)) install.packages("tidyverse")
library(tidyverse)

if (!require(tidycensus)) install.packages("tidycensus")
library(tidycensus)

### Parameters
source("credentials.R")
census_api_key(my_census_api_key)

table_census_vars <- 
	c(
		pop_total          = "B03002_001",
		pop_num_white      = "B03002_003",
		pop_num_black      = "B03002_004",
		pop_num_native     = "B03002_005",
		pop_num_asian      = "B03002_006",
		pop_num_islander   = "B03002_007",
		pop_num_other      = "B03002_008",
		pop_two_plus       = "B03002_009",
		pop_num_hisp       = "B03002_012",
		med_income         = "B19013_001",
		ed_total           = "B15003_001",
		ed_less_hs_none    = "B15003_002",
		ed_less_hs_nurse   = "B15003_003",
		ed_less_hs_kind    = "B15003_004",
		ed_less_hs_one     = "B15003_005",
		ed_less_hs_two     = "B15003_006",
		ed_less_hs_three   = "B15003_007",
		ed_less_hs_four    = "B15003_008",
		ed_less_hs_five    = "B15003_009",
		ed_less_hs_six     = "B15003_010",
		ed_less_hs_seven   = "B15003_011",
		ed_less_hs_eight   = "B15003_012",
		ed_less_hs_nine    = "B15003_013",
		ed_less_hs_ten     = "B15003_014",
		ed_less_hs_eleven  = "B15003_015",
		ed_less_hs_twelve  = "B15003_016",
		ed_hs_hs           = "B15003_017",
		ed_hs_ged          = "B15003_018",
		ed_hs_some_college = "B15003_019",
		ed_hs_college_nf   = "B15003_020",
		ed_as              = "B15003_021",
		ed_bs              = "B15003_022",
		ed_ms              = "B15003_023",
		ed_prof            = "B15003_024",
		ed_phd             = "B15003_025",
		emp_total          = "B23025_002",
		emp_unemp          = "B23025_005"
	)

table_geos <-
	tibble(
		state = c("California", "Illinois", "Massachusetts"),
		counties = list(
			as.list(c("Marin County", "San Mateo County", "San Francisco County")), 
			as.list("Cook County"), 
			as.list(c("Suffolk County", "Middlesex County"))
		)
	)

#===============================================================================

### Functions

# This function takes the raw tidycensus data and tranforms into our desirable format.
transform_census_data <- function(data, st, cty) {
	
	data %>% 
		group_by(NAME) %>%
		spread(key = variable, value = estimate) %>%
		ungroup() %>% 
		transmute(
			geoid = GEOID,
			state_fip = str_sub(geoid, 1L, 2L),
			county_fip = str_sub(geoid, 3L, 5L),
			tract_fip = str_sub(geoid, 6L, 11L),
			block_group_fip = str_sub(geoid, 12L, 12L),
			area_name = NAME,
			state = st,
			county = cty,
			#geometry,
			pop_total,
			pop_white_p = pop_num_white/pop_total,
			pop_black_p = pop_num_black/pop_total,
			pop_hisp_p = pop_num_hisp/pop_total,
			pop_asian_p = pop_num_asian/pop_total,
			pop_two_plus_p = pop_two_plus/pop_total,
			pop_other_p = pop_num_other/pop_total,
			pop_native_p = pop_num_native/pop_total,
			pop_islander_p = pop_num_islander/pop_total,
			pop_nonwhite_p = 1 - pop_white_p,
			emp_unemp_p = emp_unemp/emp_total,
			emp_emp_p = 1 - emp_unemp_p,
			ed_grad_p = (ed_prof + ed_phd + ed_ms)/ed_total,
			ed_bs_p = ed_bs/ed_total,
			ed_as_p = ed_as/ed_total,
			ed_hs_p = (ed_hs_college_nf + ed_hs_ged + ed_hs_hs + ed_hs_some_college)/ed_total,
			ed_less_hs_p = 1 - (ed_grad_p + ed_bs_p + ed_as_p + ed_hs_p),
			med_income
		)
}

### Get Data

data_census <- tibble()

for (st in table_geos$state) {
	
	counties <- table_geos %>% filter(state == st) %>% pull(counties) %>% unlist()
	
	for (cty in counties) {
		
		data_census <- 
			get_acs(
				geography = "block group",
				variables = table_census_vars,
				state = st,
				county = cty,
				year = 2015,
				geometry = FALSE
			) %>% 
			select(-moe) %>% 
			transform_census_data(st, cty) %>% 
			bind_rows(data_census)
		
	}
}

data_census %>%
	write_tsv(path = "./data/census/census_data.tsv.gz")
