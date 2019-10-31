#!/usr/bin/env python3

from itertools import groupby
from operator import itemgetter
import sys
import pandas as pd

# Parameters
DATE_INDEX = 0
HOUR_INDEX = 1
HACK_INDEX = 2
T_ONDUTY_INDEX = 3
T_OCCUPIED_INDEX = 4
N_PASS_INDEX = 5
N_TRIP_INDEX = 6
N_MILE_INDEX = 7
EARNINGS_INDEX = 8

# Function to return generator for key-value pairs in mapper/sort input
def read_mapper_output(input_stream, separator='\t'):
    for line in input_stream:
        yield line.rstrip().split(separator, 1)

def print_line(date, hour, drivers_onduty, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings):
        t_onduty_str = '%.3f' % (t_onduty)
        t_occupied_str = '%.3f' % (t_occupied)
        n_pass_str = n_pass
        n_trip_str = n_trip
        n_mile_str = '%.3f' % (n_mile)
        earnings_str = '%.2f' % (earnings)
        print(date, hour, drivers_onduty, t_onduty_str, t_occupied_str, n_pass_str, n_trip_str, n_mile_str, earnings_str, sep = ",")
        
def main(separator='\t'):
    print("date, hour, drivers_onduty, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings")
    data = read_mapper_output(sys.stdin, separator = separator)
    
    # Iterate through all hours in a the data
    for hour, all_trips in groupby(data, itemgetter(0)):
        if (hour != ""):
            drivers_onduty = 0
            t_onduty = 0
            t_occupied = 0
            n_pass = 0
            n_trip = 0
            n_mile = 0.0
            earnings = 0.0
            
            # Iterate through all trips in the given hour and calculate summary statistics
            for trip in all_trips:
                trip_details = trip[1].split(",")
                date = trip_details[DATE_INDEX]
                hour = trip_details[HOUR_INDEX]
                drivers_onduty += 1
                t_onduty += float(trip_details[T_ONDUTY_INDEX])
                t_occupied += float(trip_details[T_OCCUPIED_INDEX])
                n_pass += int(trip_details[N_PASS_INDEX])
                n_trip += int(trip_details[N_TRIP_INDEX])
                n_mile += float(trip_details[N_MILE_INDEX])
                earnings += float(trip_details[EARNINGS_INDEX])

            print_line(date, hour, drivers_onduty, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings)    


if __name__ == "__main__":
    main()
