################################################################################
## Author: Michael Spencer, Andrew (Foster) Docherty, Jorge Nam Song,
##         Lauren Feitzinger, Andrea Banuet
## Project: MS&E 231 - 311 Calls
## Script Purpose: Convert shapefiles as geojson for Mapbox
## Notes: May be slow
################################################################################

# Libraries
if (!require(sf)) install.packages("sf")
library(sf)

if (!require(tidyverse)) install.packages("tidyverse")
library(tidyverse)

print("Writing summary files to geojson...")

# Transform data into summary stats for each census tract
data_calls %>% 
	group_by(geoid, topic) %>% 
	summarize(
		num_topic = n(),
		human = sum(req_aim == "human", na.rm = TRUE),
		non_human = sum(req_aim == "non-human", na.rm = TRUE),
		illegal = sum(illegal == "yes", na.rm = TRUE),
		not_illegal = sum(illegal == "no", na.rm = TRUE),
		adversarial = sum(adv == "yes", na.rm = TRUE),
		not_adversarial = sum(adv == "no", na.rm = TRUE)
	) %>% 
	mutate(
		total_reqs = sum(num_topic, na.rm = TRUE),
		prop_human = sum(human, na.rm = TRUE)/total_reqs,
		prop_nonhuman = sum(non_human, na.rm = TRUE)/total_reqs,
		prop_illegal = sum(illegal, na.rm = TRUE)/total_reqs,
		prop_legal = sum(not_illegal, na.rm = TRUE)/total_reqs,
		prop_adv = sum(adversarial, na.rm = TRUE)/total_reqs,
		prop_not_adv = sum(not_adversarial, na.rm = TRUE)/total_reqs
	) %>% 
	group_by(topic) %>% 
	mutate(prop_topic = num_topic/total_reqs) %>% 
	select(-num_topic, -human, -non_human, -illegal, -not_illegal, -adversarial, -not_adversarial) %>% 
	ungroup() %>% 
	spread(topic, prop_topic) %>% 
	
	# Join data with census metrics
	left_join(data_descriptive, by = "geoid") %>% 
	mutate(avg_num_reqs = total_reqs/pop_tot) %>% 
	st_sf() %>% 
	
	# Write to geojson for Mapbox
	write_sf(
		paste0(project_dir, "/data/311/", data_city, "/", data_name, ".geojson"), 
		delete_layer = TRUE,
		delete_dsn = TRUE
	)

print("Summary geojson files written!")