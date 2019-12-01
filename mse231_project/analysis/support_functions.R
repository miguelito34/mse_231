################################################################################
## Author: Michael Spencer, Andrew (Foster) Docherty, Jorge Nam Song,
##         Lauren Feitzinger, Andrea Banuet
## Project: MS&E 231 - 311 Calls
## Script Purpose: Load supporting functions for analysis scripts
## Notes: Includes plotting and mapping functions
################################################################################

############################## Plotting Functions ##############################
# Gets the minimum of a given metric
get_min <- function(metric) {
	metric <- data_summary %>% pull(metric)
	range(metric, finite = TRUE)[1]
}

# Gets the maximium of a given metric
get_max <- function(metric) {
	metric <- data_summary %>% pull(metric)
	range(metric, finite = TRUE)[2]
}

# Finds the 95 percentile
find_outlier <- function(metric) {
	data_summary %>% pull(metric) %>% quantile(.95, names = FALSE, na.rm = TRUE)
}

# Provides proper breaks to scales
get_break_width <- function(metric) {
	((find_outlier(metric) - get_min(metric))/8)
}

get_breaks <- function(metric) {
	seq(get_min(metric), find_outlier(metric), get_break_width(metric))
}

############################### Mapping Functions ##############################

# Quantile for Mapbox Coloring
# vars_to_pull <- 
# 	data_summary %>% 
# 	select(-geoid, -st_fip, -trt_fip, -cty_fip, -state, -geometry, -detail) %>% 
# 	colnames()
# 
# find_colors <- function(v, q) {
# 	quantile(v, seq(0, 1, .125), na.rm = TRUE, names = FALSE)
# }
# 
# data_color_info <- matrix(data = 0, nrow = 9, ncol = length(vars_to_pull))
# 
# for (i in 1:length(vars_to_pull)) {
# 	
# 	v <- vars_to_pull[i]
# 	
# 	data <-
# 		data_summary %>%
# 		pull(v) %>%
# 		find_colors(v)
# 	
# 	data_color_info[,i] <- data
# 	
# }
# 
# data_color_info <- data_color_info %>% as_tibble()
# 
# colnames(data_color_info) <- vars_to_pull
# 
# data_color_info <- 
# 	data_color_info %>% 
# 	mutate(
# 		prob = c(0, .125, .25, .375, .5, .625, .75, .875, 1),
# 		color = c("#004364", "#195473", "#55889e", "#a2c0a1", "#fdf6a3", ".#e9b777", ".#d27952", "#b63132", "#740023")
# 	)

# data_color_info %>% 
# 	select(color, prob, everything()) %>% 
# 	write_tsv(paste0(project_dir, "/docs/", data_city, "_color_encodings",".tsv"))
