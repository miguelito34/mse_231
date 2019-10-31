MS&E 231 HW2 README

# Authors:
Andrew (Foster) Docherty, Michael Spencer, Jorge Nam

# Objective and approach:
The current directory includes Python3 scripts that as a whole serve as a solution to converting data on taxi rides in New York City from 2010 to 2013 into aggregated fields of interest on these rides. These fields are then used in our analysis in conversation with Farber and of Camerer et al. on the question of "Why is it so hard to catch a cab in the rain?" Below, we detail how we executed this conversion via three consecutive MapReduce operations.

# MapReduce operations (files and brief descriptions):

## MapReduce 1: Join and preliminary cleaning
Given that the relevant NYC taxi data was initially stored in two separate tables, namely the "trip" and "fare" data, we first had to join the datasets into one.

### join_map.py
In the mapping step, we use each driver's hack licence (provided on a yearly basis) and the pickup date-time of the trip as the key to uniquely identify trips. The value then was the full data from the original table, as well as a flag indicating which table the row originated from.

### join_reduce.py
In the reducing step, we joined the unique data from each row of "trip" and "fare" data into one row. In addition, we applied a number of cleaning operations, such as dropping rows with erroneous data (e.g. coordinates of zero) and correcting any potentially unreliable data (e.g. trip duration in seconds via calculating the time between dropoff and pickup).

## MapReduce 2: Grouping by date and hour
Using the joined data, we then grouped by date and hour for each driver to calculate fields of interest for our analysis.

### driver_stats_map.py
In the mapping step, we split the data into hours of the day, for example converting a 3:30-4:30pm trip into a 3:30-4pm and 4-4:30pm trip. We also use a dual-key mapping approach by using both the hack license + year and the pickup date-time as keys. The hack license + year key is printed first, used to map and sort the data. We then print a pickup-date time key to be used in the reducer for grouping by date and hour.

### driver_stats_reduce.py
In the reducing step, we calculate the fields we are interested in for our analysis, namely t_onduty, t_occupied, n_pass, n_trip, n_mile, and earnings. These fields are all relatively simple calculations given the hour-to-hour split from the mapper, with the exception being t_onduty which requires information about adjacent hours.

## MapReduce 3: Aggregation across drivers
Finally, on this data grouped by date and hour we performed a simple summation across all of the fields of interest.

### agg_hourly_stats_map.py
In the mapping step, we simply mapped each row by using the date and hour as the key and the fields as the value.

### agg_hourly_stats_reduce.py
In the reducing step, we summed across the fields for each driver in the date-hour, resulting in aggregated values for each date-hour. This finalized data is then used in our analysis.

## Joining and Analysis
Once we had our finalized trip data, we joined it with precipitation data.

### step_6_join.R
In this joining script, we simply load in the relevant trip and precipitation data, modify the date and hours columns to ensure they can be joined, and join.

### step_7_analysis.pdf
In this script we explore the effects of rain on wages, supply, and demand. For supply, we used the following metrics: the average number of on-duty hours in a given hour, and the average proportion of the hour drivers spent on-duty.For demand, we explored four metrics: the average hourly number of passengers, the average number of taxi trips, the average number of passengers per trip, and the utilization of taxis in a given hour.