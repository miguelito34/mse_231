################################################################################
## Author: Michael Spencer, Andrew (Foster) Docherty, Jorge Nam Song,
##         Lauren Feitzinger, Andrea Banuet
## Project: MS&E 231 - 311 Calls
## Script Purpose: Match the 311 call data to a given complaint category
## Notes: Complaints are currently categorized as human or non-human though
##        further categorization may be needed.
################################################################################

### Parameters
# Will read from Google Sheets so ensure sheet is updated and stable
path_categories <- "https://docs.google.com/spreadsheets/d/16_G3nBNMg3H88tBs2i8BO1enHWza5p8tyM_giACXvPM/edit#gid=0"
path_data_shapefiles <- paste0(project_dir, "/data_raw/311/joined/", data_name, ".shp")

print("Getting info to match calls to request categories...")

### Load  and Join Data
data_categories <- 
    path_categories %>% 
    read_sheet() %>% 
    select(-explain)

data <- 
    path_data_shapefiles %>% 
    st_read() %>% 
    mutate(city = str_extract(city, pattern = ".+(?=[,_])")) %>% 
    left_join(data_categories, by = c("city", "service_na" = "req_name"))

print("Finished matching calls to complaint categories, will clean data now...")

rm("path_categories", "path_data_shapefiles", "data_categories")
