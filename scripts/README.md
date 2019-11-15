# Scripts

### Census Scripts

The `census` scripts folder contains the following scripts to aid in pulling census data:

* __load_census_query.R__: Loads the relevant variables we wish to pull from the census. If you would like to pull more variables, you will need to ask for them in this file, and make the neccessary modifications in the `pull_census_data.R` file to ensure they are not dropped. Likewise, you can change the locations for which you request data using this file. No modifications to `pull_census_data.R` are needed if only the locations requested changes.

* __pull_census_data.R__: Sources the search query from `load_census_query.R` and pulls the relevant data by block group for each location requested, compiling it into one table before writing it into the `data/census/` folder. Writes both a file with shapefiles and one without.

### 311 Scripts

The `311` scripts folder contains the following scripts to aid in pulling 311 calls from the open311 API:

* __open311_get_service_list.py__: This script accesses the open311 API and pulls down the available service requests for each city. After running this script, the relevant data file can be found at `data/311/service_requests.csv`. These requests will later be categorized for analysis.

* __open311_pull_all_data.py__: This script currently accesses and downloads all 311 requests for 2019 from the cities in the analysis. The relevant data file can be found at `raw_data/311/sample_311_data.tsv`. This will change and grow as analysis continues.

* __get_census_tract.py__: This script streams each 311 request downloaded and determines the census tract that the request occured in by querying Census Geocoding Services. The script is currently slow and further work is needed to accelerate it. Such location determination will aid in later analysis.