# Scripts

### Census Scripts

The `census` scripts folder contains the following scripts to aid in pulling census data:

* __load_census_query.R__: Loads the relevant variables we wish to pull from the census. If you would like to pull more variables, you will need to ask for them in this file, and make the neccessary modifications in the `pull_census_data.R` file to ensure they are not dropped. Likewise, you can change the locations for which you request data using this file. No modifications to `pull_census_data.R` are needed if only the locations requested changes.

* __pull_census_data.R__: Sources the search query from `load_census_query.R` and pulls the relevant data by block group for each location requested, compiling it into one table before writing it into the `data/census/` folder. Writes both a file with shapefiles and one without.
