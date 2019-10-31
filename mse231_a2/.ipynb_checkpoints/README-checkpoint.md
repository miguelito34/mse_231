# MSnE231-HW2

## I. Steps to replicate Step 3 local test
1. Clone the repo in a directory of your choosing (I would recommend making one on Farmshare):
```
mkdir HW2
cd HW2
git init
git remote add origin https://github.com/afdocherty/MSnE231-HW2.git
git pull origin master
(Enter your GitHub credentials)
```

2. Pull the Step 2 data with:
```
wget https://5harad.com/data/nyctaxi/2013_trip_data_1.csv.gz 
wget https://5harad.com/data/nyctaxi/2013_fare_data_1.csv.gz 
```

3. Get only the 1st day (Jan 1st) of the data:
```
zcat 2013_fare_data_1.csv.gz | python3 step_2_fare.py > 2013-01-01_fare_data.csv
zcat 2013_trip_data_1.csv.gz | python3 step_2_trip.py > 2013-01-01_trip_data.csv
```

4. Run the MapReduce job locally:
```
cat 2013-01-01_trip_data.csv 2013-01-01_fare_data.csv | python3 join_map.py | sort | python3 join_reduce.py > results_join_reduce_test.csv
```

5. Look at the first and last lines of the output file:
```
head results_join_reduce_test.csv
tail results_join_reduce_test.csv
```

6. You can test Part 4 code on this data. For super simple tests, you can make a file with just the head:
```
head results_join_reduce_test.csv > results_join_reduce_test_head.csv
```

8. If you are accessing the fields in each line via .split(","), you can use this mapping of variables to indices (contained in join_reduce.py):
```python
# Mapping of variables to indices for joined dataset
MEDALLION_INDEX = 0
HACK_LICENSE_INDEX = 1
VENDOR_ID_INDEX = 2
RATE_CODE_INDEX = 3
STORE_AND_FWD_FLAG_INDEX = 4
PICKUP_DATETIME_INDEX = 5
DROPOFF_DATETIME_INDEX = 6
PASSENGER_COUNT_INDEX = 7
TRIP_TIME_IN_SECS_INDEX = 8
TRIP_DISTANCE_INDEX = 9
PICKUP_LONGITUDE_INDEX = 10
PICKUP_LATITUDE_INDEX = 11
DROPOFF_LONGITUDE_INDEX = 12
DROPOFF_LATITUDE_INDEX = 13
PAYMENT_TYPE_INDEX = 14
FARE_AMOUNT_INDEX = 15
SURCHARGE_INDEX = 16
MTA_TAX_INDEX = 17
TIP_AMOUNT_INDEX = 18
TOLLS_AMOUNT_INDEX = 19
TOTAL_AMOUNT_INDEX = 20
```

## II. Steps to replicate Step 4 local test after following relevant instructions above
1. Within the proper directory (i.e where all of the files are), run the following terminal command to save the output (this may take 4-5 minutes):
```
cat results_join_reduce_test.csv | ./driver_stats_map.py | sort | ./driver_stats_reduce.py > results_step_4_test.csv
```

## III. Steps to replicate Step 5 local test after following relevant instructions above
1. Within the proper directory (i.e where all of the files are), run the following terminal command to glimpse the structured output:
```
cat results_step_4_test.csv | ./agg_hourly_stats_map.py | sort | ./agg_hourly_stats_reduce.py > results_step_5_test.csv
```
