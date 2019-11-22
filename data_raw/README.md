# Raw Data

### 311

After running the relevant scripts per the in the project README, the `311/unjoined/` raw data folder contains the raw 311 call data that was downloaded:

* __<data_version>.tsv__: A sample of the raw data pulled from the open311 API for all relevant US cities included in our analysis.

After running the relevant scripts per the project README, the `311/joined/` raw data folder contains the 311 data joined with the relevant census data. This is also where you can find shapefiles and the files to be cleaned for analysis:

* __<data_version.shp__: The same file as above but intersected with census tract shapefiles and now containing GEOID's such that each call can now be placed into a census tract for further analysis.