# Raw Data

### 311

After running the relevant scripts per the in the project README, the `311` raw data folder contains the following:

* __sample_311_data.tsv__: A sample of the raw data pulled from the open311 API for all relevant US cities included in our analysis.

* __sample_311_data_geoid.tsv__: The same file as above passed through the [Census Geocoding API](https://www.census.gov/programs-surveys/geography/technical-documentation/complete-technical-documentation/census-geocoder.html), and now containing GEOID's such that each call can now be placed into a census tract for further analysis.