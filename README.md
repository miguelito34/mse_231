# Analyzing Bias and Disparities in 311 Calls

### Overview
We will analyze 311 calls to answer the following question: do we see a higher volume of disturbance or conflict-centered 311 requests in city neighborhoods associated with and high proportions of people of color?

### Getting Set Up

1. Folder Structure

* __data__: cleaned data
* __data_raw__: raw data
* __docs__: data documentation and notes
* __analysis__: exploratory data analysis on your cleaned data
* __scripts__: data-cleaning scripts
* __reports__: findings to present to others

2. Clone the GitHub repo into a directory of your choosing. You can name the directory whatever you'd like.
```
mkdir <your new folder>
cd <your new folder>
git init
git remote add origin git@github.com:afdocherty/MSnE231-Project.git
git pull origin master
```

3. The first time you go to push a file, you may receive this note:
```
fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master
```

If you see that, push using the instructions as above:
```
git push --set-upstream origin master
```

From now on, anytime you need to make changes, you should be able to push using:
```
git push
```

4. Make a credentials file

In the project directory, create a new R script called `credentials.R`. Include the following lines with the relevant credentials:
```
my_census_api_key <- "<YOUR CENSUS API KEY>"
```

Follow the relevant links to sign up for any needed credentials you don't already have or cannot supply:

* my_census_api_key: [get API key here](https://api.census.gov/data/key_signup.html)

### Data

The data for this project are pulled from many different sources. You can find a link to each source below:

* __311 Data__: 311 data was pulled using the [open311](https://www.open311.org/) database. The cities used in the analysis can be found below. 
	* San Francisco, CA
	* Chicago, IL
	* Peoria, IL
	* Bloomington, IN
	* Boston, MA
	* Brookline, MA

* __The US Census__: Data was pulled from the [US Census](https://data.census.gov/cedsci/?intcmp=aff_cedsci_banner) via the R package [tidycensus](https://walkerke.github.io/tidycensus/), which allows for easy access to the Census API.

* __Census Geocoding__: The census tract for each 311 request was determined using [Census Geocoding Services](https://www.census.gov/programs-surveys/geography/technical-documentation/complete-technical-documentation/census-geocoder.html).

### Replication

1. Download the census data

To download the relevant census data, assuming you have set up a credentials file, you can run the following command from an R kernel within the project directory:
```
Rscript scripts/census/pull_census_data.R
```

2. View the available 311 service requests

To see the available service requests in each city, run the following python script from within the project directory:
```
python3 scripts/311/open311_get_service_list.py
```

3. Download a sample of the available 311 calls

Adjusts to this step will be made as the quantity of calls available/needed changes. In the future, this step will likely be piped into the following step so as to output a single file that includes the calls as well as their census tracts. To replicate, run the script as below:
```
python3 scripts/311/open311_pull_all_data.py > data_raw/311/sample_311_data.tsv
```

4. Locate each call

In order to perform any significant analysis, we must join this call data with census data. We'll be doing this at the level of census tracts. This script will pair each call with it's relevant geoid, allowing us to join the call with census data in later steps. In this step, we discard any calls for which the location cannot be determined by lat/long.
```
python3 scripts/311/get_census_tract.py > data_raw/311/sample_311_data_geoid.tsv
```

### Approach and Strategy (To Come)

### Results (To Come)

### Conclusions and Limitations (To Come)
