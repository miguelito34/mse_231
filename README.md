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

### Replication

1. Download the data

To download the relevant census data, assuming you have set up a credentials file, you can run the following command from the project directory:
```
source("scripts/census/pull_census_data.R")
```

### Data

### Approach and Strategy

### Results

### Conclusions and Limitations
