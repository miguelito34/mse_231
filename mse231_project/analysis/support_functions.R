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
	metric <- enquo(metric)
	metric <- data_summary %>% pull(!!metric)
	range(metric, finite = TRUE)[1]
}


# Gets the maximium of a given metric
get_max <- function(metric) {
	metric <- enquo(metric)
	metric <- data_summary %>% pull(!!metric)
	range(metric, finite = TRUE)[2]
}


# Finds the 95 percentile
find_outlier <- function(metric) {
	metric <- enquo(metric)
	data_summary %>% pull(!!metric) %>% quantile(.95, names = FALSE, na.rm = TRUE)
}


# Provides proper breaks to scales
get_break_width <- function(metric) {
	metric <- enquo(metric)
	((find_outlier(!!metric) - get_min(!!metric))/8)
}


# Calculates sequence of breaks
get_breaks <- function(metric) {
	metric <- enquo(metric)
	seq(get_min(!!metric), find_outlier(!!metric), get_break_width(!!metric))
}


############################### Mapping Parameters #############################

# Color used for mapping gradient
MAP_COLORS <- c(
	"#740023",
	"#b63132",
	"#d27952",
	"#e9b777",
	"#fdf6a3",
	"#a2c0a1",
	"#55889e",
	"#195473",
	"#004364"
)


# Color used for missing values
MAP_NA_COLOR <- "#f2f2f2"

############################### Mapping Functions ##############################

get_quartile_breaks <- function(metric) {
	metric <- enquo(metric)
	data_summary %>% 
		mutate_outliers(!!metric) %>% 
		pull(!!metric) %>% 
		quantile(seq(0, 1, .125), na.rm = TRUE, names = FALSE)
}


# Makes outliers equal to the 95 percentile to avoid outlandish scales. Note this in writeup.
mutate_outliers <- function(df, metric) {
	metric <- enquo(metric)
	df %>% 
		mutate(
			!!metric := 
				ifelse(
					(!!metric) <= find_outlier(!!metric), 
					!!metric, 
					find_outlier(!!metric)
				)
		)
}


# Finds basemap for current city
find_basemap <- function() {
	if (data_city == "SFO") {
		bb <- c(left = -122.52, bottom = 37.66, right = -122.35, top = 37.82)
	} else if (data_city == "CHI") {
		bb <- c(left = -88.008, bottom = 41.632, right = -87.463, top = 42.047)
	} else if (data_city == "BOS") {
		bb <- c(left = -71.245, bottom = 42.181, right = -70.908, top = 42.426)
	}
	
	basemap <- 
		get_stamenmap(
			bbox = bb, 
			zoom = 12,
			maptype = "toner-lines"
		)
}


# Properly formats the scale based on the metric
get_scale_formatting <- function(metric_type) {
	if (metric_type == "number") {
		scales::number_format(accuracy = .01, big.mark = ",")
	} else if (metric_type == "percent") {
		scales::percent_format(accuracy = .1, big.mark = ",")
	} else if (metric_type == "rent") {
		scales::comma_format(accuracy = 100, prefix = "$")
	} else if (metric_type == "value") {
		scales::comma_format(accuracy = 1000, prefix = "$")
	} else {
		scales::number_format()
	}
}


# Reverses the color scale when appropriate
rev_colors <- function(rev_scale) {
	if (rev_scale == "higher is better") return(MAP_COLORS)
	rev(MAP_COLORS)
}


get_full_city_name <- function() {
	case_when(
		data_city == "SFO" ~ "San Francisco",
		data_city == "CHI" ~ "Chicago",
		data_city == "BOS" ~ "Boston"
	)
}


make_map <- function(metric, rev_scale = 0, metric_type, map_title = data_city, legend_title = "Metric") {
	
	metric <- enquo(metric)
	
	ggmap(find_basemap()) +
	geom_sf(
		data = data_summary %>% mutate_outliers(!!metric) %>% st_sf(),
		aes(fill = !!metric), 
		color = "white", 
		size = .1, 
		alpha = .8,
		inherit.aes = FALSE
	) +
	scale_fill_gradientn(
		colors = rev_colors(rev_scale),
		values = get_quartile_breaks(!!metric) %>% scales::rescale(),
		na.value = MAP_NA_COLOR,
		labels = get_scale_formatting(metric_type)
	) +
	theme_void() +
	theme(
		legend.position = "bottom",
		legend.text = element_text(size = 7),
		legend.margin = margin(b = 10),
		plot.caption = element_text(hjust = .5),
		legend.title = element_text(size = 10),
		plot.title = element_text(hjust = 0.5)
	) +
	guides(
		fill =
			guide_colorbar(
				title = legend_title,
				title.position = "top",
				barwidth = 15,
				barheight = .25,
				nbin = 16,
				raster = TRUE,
				ticks = TRUE
			)
	) +
	labs(
		title = map_title,
		caption = "NOTE: Outliers were consolidated."
	)
}	