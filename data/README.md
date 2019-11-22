# Data

### Census Data

After running the relevant scripts per the in the project README, the `census` data folder contains the following:

* __census_data.tsv.gz__: The formatted census data by block group containing information about race/ethnicity, income, education, and employment.

* __census_data_shapefiles.shp__: Similar data as `census_data.tsv.gz`, but with the relevant shapefile for a given block group.

### 311

After running the relevant scripts per the in the project README, the `311` data folder contains the following:

* __service_names.csv__: A temporary list, by city, of the 311 service requests that can be made used to get a sense of the data.

* __complaint_categorization.csv__: A full list of all services available in the data that was used in the analysis. It is constantly updated and pulled from a collaborative [Google Sheet](https://docs.google.com/spreadsheets/d/16_G3nBNMg3H88tBs2i8BO1enHWza5p8tyM_giACXvPM/edit?usp=sharing). Prior to running the analysis, ensure you have the latest sheet downloaded. The determinations in this sheet were subjective, but vetted by the entire team. Categories can be found below:
    * _Request (`req_name`)_: The raw name of the possible requests in the data.
    * _Request aim (`req_aim`)_: This denotes the target of the request, whether a human (themselves, their actions, or their belongings) or a non-human entity.
    * _Legality of the event/concern reported (`legal`)_: This denotes whether or not the reported incident/concern regards a potentially illegal matter such as illegal graffiti, trash dumping, parking, etc.
    * _Adversarial nature of request (`adv`)_: This denotes whether or not a given request is adversarial to another person (themselves, their actions, their belongings of that being, or the area that that being resides in/near). In this case, we are referring to fellow citizens, and not neccessarily city entities, or citizens working on behalf of the government.
    * _Categorized topic of request (`topic`)_: This denotes the umbrella category that a given request was grouped under. While we strived to make these grouping mutually exclusive and collectively exhaustive, they may not always be. 

* __<data_version>_clean.tsv__: Prepped and cleaned data ready for analysis. A version with shapefiles can be found in the `.shp` file below.
    
* __<data_version>_clean.shp__: Prepped and cleaned 311 data ready for analysis; includes shapefiles.
