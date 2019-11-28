# Scripts

### Census Scripts

The `census` scripts folder contains the following scripts to aid in pulling census data:

* __load_census_query.R__: Loads the relevant variables we wish to pull from the census. If you would like to pull more variables, you will need to ask for them in this file, and make the neccessary modifications in the `pull_census_data.R` file to ensure they are not dropped. Likewise, you can change the locations for which you request data using this file. No modifications to `pull_census_data.R` are needed if only the locations requested changes.

* __pull_census_data.R__: Sources the search query from `load_census_query.R` and pulls the relevant data by block group for each location requested, compiling it into one table before writing it into the `data/census/` folder. Writes both a file with shapefiles and one without.

### 311 Scripts

The `311` scripts folder contains the following scripts to aid in pulling 311 calls from the open311 API:

* __open311_get_service_list.py__: This script accesses the open311 API and pulls down the available service requests for each city. After running this script, the relevant data file can be found at `data/311/service_requests.csv`. These requests will later be categorized for analysis.

* __open311_pull_all_data.py__: This script currently accesses and downloads all 311 requests for 2019 from the cities in the analysis. The relevant data file can be found at `raw_data/311/sample_311_data.tsv`. This will change and grow as analysis continues.

* __get_census_tract_batch.py__: This script batch processes 311 request downloads and determines the census tract that the request occured in by determining which census tract the call is within. This script is currently preferred to the two streaming scripts below as it is much faster for our current scale. Such location determination will aid in later analysis.

* __get_census_tract_stream.py__: This script streams each 311 request downloaded and determines the census tract that the request occured in by querying the FCC Area API. The script is currently a bit slow and further work is needed to accelerate it. Such location determination will aid in later analysis.

* __join_census.py__: This is the streaming alternative to `get_census_tract_batch.py` should a streaming approach be preffered due to scale limitations. This file uses census tracts to match each call with relevant census demographic data.

* __find_complaint_categories.R__: This script categorizes the joined 311/census data, categorizing calls by whether or not they were human-oriented, adversarial, etc. This script feeds data into the `final_clean.R` script below, which cleans and preps the data prior to writing it out and loading it for the analysis scripts. Categorization of calls was done manually by the team in [Google Sheets](https://docs.google.com/spreadsheets/d/16_G3nBNMg3H88tBs2i8BO1enHWza5p8tyM_giACXvPM/edit?usp=sharing).

* __final_clean.R__: This script performs a final cleaning and prepping of the data prior to analysis. It keeps the data loaded in the environment to reduce time loading in, but also writes out the files for later use in other software.