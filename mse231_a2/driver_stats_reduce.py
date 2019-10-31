#!/usr/bin/env python3

# Imports
from itertools import groupby
from operator import itemgetter
import sys
import datetime as dt

# Constants
MEDALLION_INDEX = 0
HACK_LICENSE_INDEX = 1
PICKUP_DATETIME_INDEX = 5
DROPOFF_DATETIME_INDEX = 6
PASSENGER_COUNT_INDEX = 7
TRIP_TIME_IN_SECS_INDEX = 8
TRIP_DISTANCE_INDEX = 9
TOTAL_AMOUNT_INDEX = 20


def get_group_info(driver, hour):
    """Function to retireve the date, hour, and hack from the group key"""
    split_hour = hour.split(" ")
    return split_hour[0], split_hour[1], driver


def break_in_same_hour(current_pickup_time, prev_dropoff_time):
    """
    Determines if a given break in a driver's trip records is within a single hour or multiple hours, 
    determines how we process and partition timeonduty (t_onduty)
    """
    current_pickup_time = dt.datetime.strptime(current_pickup_time, "%Y-%m-%d %H:%M:%S")
    prev_dropoff_time = dt.datetime.strptime(prev_dropoff_time, "%Y-%m-%d %H:%M:%S")
    return (current_pickup_time.hour == prev_dropoff_time.hour)


def non_occupied_t_onduty(current_pickup_time, prev_dropoff_time, calc_for_hour):
    """
    Function to calculate and partition the time on-duty (t_onduty) dependent 
    on the span of the break as found in "break_in_same_hour"
    """
    current_pickup_time = dt.datetime.strptime(current_pickup_time, "%Y-%m-%d %H:%M:%S")
    prev_dropoff_time = dt.datetime.strptime(prev_dropoff_time, "%Y-%m-%d %H:%M:%S")
    
    # Calculates the length of a break between trips
    break_time = (current_pickup_time - prev_dropoff_time).total_seconds()/3600
    
    # Determines if the driver was on-duty during the break (i.e. the break was 30 minutes or less which 
    # is assumed to mean the driver was actively driving and searching for more trips). Partitions this time depending
    # on the span of the break
    if (break_time < .5):
        if (calc_for_hour == "same"):
            return break_time
        elif (calc_for_hour == "prev" and break_time != 0.0): 
            # Partitions time and adds to t_onduty sum for previous hour
            return float((prev_dropoff_time.replace(microsecond=0,second=0,minute=0) + dt.timedelta(hours=1) - prev_dropoff_time).total_seconds()/3600)
        else: 
            # Partitions time and adds to t_onduty sum for current hour
            return float((current_pickup_time - current_pickup_time.replace(microsecond=0,second=0,minute=0)).total_seconds()/3600)
    else:
        return 0.0

    
def read_mapper_output(input_stream, separator='\t'):
    """Function to return generator for key-value pairs in mapper/sort input"""
    for line in input_stream:
        yield line.rstrip().split(separator, 2)
        
        
def increment_fields(trip_details, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings):
    """Sums relevant values while iterating over trips"""
    t_onduty += float('%.3f' % (float(int(trip_details[TRIP_TIME_IN_SECS_INDEX])/3600)))
    t_occupied += int(trip_details[TRIP_TIME_IN_SECS_INDEX])
    n_pass += int(trip_details[PASSENGER_COUNT_INDEX])
    n_trip += int(1 if (trip_details[PASSENGER_COUNT_INDEX] != "0") else 0)
    n_mile += float(trip_details[TRIP_DISTANCE_INDEX])
    earnings += float(trip_details[TOTAL_AMOUNT_INDEX])
    return t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings

 
def print_line(date, prev_hour, hack, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings):
    """Function to format line based on args and print it"""
    t_onduty_str = '%.3f' % (t_onduty)
    t_occupied_str = '%.3f' % (float(t_occupied/3600))
    n_pass_str = n_pass
    n_trip_str = n_trip
    n_mile_str = '%.3f' % (n_mile)
    earnings_str = '%.2f' % (earnings)
    print(date, prev_hour, hack, t_onduty_str, t_occupied_str, n_pass_str, n_trip_str, n_mile_str, earnings_str, sep = ",")

        
def main(separator='\t'):
    # Print header
    print("date, hour, hack, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings")
    
    data = read_mapper_output(sys.stdin, separator = separator)
    
    # Iterate through all stops made by a given driver in the year
    for driver, all_trips in groupby(data, itemgetter(0)):
        t_onduty = 0
        n_trip = 0
        t_occupied = 0
        n_pass = 0
        n_mile = 0.0
        earnings = 0.0
        prev_dropoff_time = ""
        prev_date = ""
        prev_hour = ""
        
        # Iterate through all hours driven by a given driver in the year
        for hour, hour_trips in groupby(all_trips, itemgetter(1)):
            date, hour, hack = get_group_info(driver, hour)
            
            # Iterate through all stops made by a given driver in a given hour
            for trip in hour_trips:
                trip_details = trip[2].split(",")
                
                # Check if this is driver's first trip in record and adds relevant metrics to hourly sums
                # NOTE: Assumes any time before this, the driver was off-duty (i.e if the first recorded trip starts at 3:15pm,
                # we assume the driver was off-duty prior to 3:15pm)
                if (prev_dropoff_time == ""):
                    t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings = increment_fields(trip_details, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings)
                # Given the trip isn't the first in the record, calculates t_onduty for trips dependent on whether a break in driving
                # crossed an hour boundary and whether the driver was on or off-duty
                else:
                    
                    # Checks to see if the break is within a single hour
                    if (break_in_same_hour(trip_details[PICKUP_DATETIME_INDEX], prev_dropoff_time) and trip_details[PASSENGER_COUNT_INDEX] != "0"):
                        
                        # Is the driver on-duty within this break and if so, add time to t_onduty for the current hour
                        t_onduty += non_occupied_t_onduty(trip_details[PICKUP_DATETIME_INDEX], prev_dropoff_time, calc_for_hour = "same")
                        
                    # Else the break crosses an hour boundary meaning we can finish calculating info for the previous trip, 
                    # print it, and reset variables for the current hour's calculations
                    else:
                        # Add on-duty time to previous hour
                        t_onduty += non_occupied_t_onduty(trip_details[PICKUP_DATETIME_INDEX], prev_dropoff_time, calc_for_hour = "prev")
                        
                        # Print previous hour only if the driver was on-duty
                        if (t_onduty > 0):
                            print_line(prev_date, prev_hour, hack, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings)
                        
                        # Reset all_variables
                        t_onduty = 0
                        n_trip = 0
                        t_occupied = 0
                        n_pass = 0
                        n_mile = 0.0
                        earnings = 0.0
                        
                        # Add on-duty time to current hour
                        t_onduty = non_occupied_t_onduty(trip_details[PICKUP_DATETIME_INDEX], prev_dropoff_time, calc_for_hour = "current")
                        
                    # Calculate variables for current hour, assuming it isn't the first trip
                    # This t_onduty is for the actual trip, not a break
                    t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings = increment_fields(trip_details, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings)
 
                # Store variables for reference when processing next trip
                prev_date = date
                prev_hour = hour
                prev_dropoff_time = trip_details[DROPOFF_DATETIME_INDEX]
        
        # Handles printing for last trip on a driver's record
        print_line(date, prev_hour, hack, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings) 
        
if __name__ == "__main__":
    main()
