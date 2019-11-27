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
	* Peoria, IL (Pending)
	* Bloomington, IN (Pending)
	* Boston, MA
	* Brookline, MA (Pending)

* __The US Census__: Data was pulled from the [US Census](https://data.census.gov/cedsci/?intcmp=aff_cedsci_banner) via the R package [tidycensus](https://walkerke.github.io/tidycensus/), which allows for easy access to the Census API.

* __FCC Geocoding__: The census tract for each 311 request was determined using [FCC Area API](https://geo.fcc.gov/api/census/#!/block/get_block_find).

### Replication

1. Download the census data

To download the relevant census data, assuming you have set up a credentials file, you can run the following command from an R kernel within the project directory:
```
Rscript scripts/census/pull_census_data.R
```

2. View the available 311 service requests

To see the available service requests in each city, visit the teams [working Google Sheet](https://docs.google.com/spreadsheets/d/16_G3nBNMg3H88tBs2i8BO1enHWza5p8tyM_giACXvPM/edit?usp=sharing)

3. 311 call data has been streamed and is available in `data_raw/311/unjoined/`. 

The next steps can be easily carried out on your local computer and rely on the provided raw data.

4. Locate each call

In order to perform any significant analysis, we must join this call data with census data. We'll be doing this at the level of census tracts. This script will pair each call with it's relevant geoid, allowing us to join the call with census data in later steps. In this step, we discard any calls for which the location cannot be determined by lat/long.

Current options for analysis are:

* San Francisco - "SFO"
* Chicago - "CHI"

```
python3 scripts/311/get_census_tract_batch.py <city abb>
```
The output data will be in `data_raw/311/joined/`.

6. Replicate the analysis or start your own

Now that you have all the data you will need, to replicate the analysis thus far run the following, substituting `<city abb>` for a city of your choosing and `<write full data>` with either "yes" or "no" depending on if you'd like to write out the full dataset for that city:
```
bash render_report <city abb> <write full data>
```

Example:
```
bash render_report CHI no
```

To perform your own analysis, you can start with the template at `analysis/template_exploratory_analysis.Rmd` by opening it in RStudio. The code already written will load the neccessary packages to read in and clean the data for analysis. Some of the data is pulled from a google sheet that the team maintains. Upon running the script, you may be asked to authenticate your google account. Doing so gives the `googlesheets4` package, which is used to pull the data, permission to access the sheet. Please follow the instructions.

### Approach and Strategy (To Come)

### Results (To Come)

### Conclusions and Limitations (To Come)
