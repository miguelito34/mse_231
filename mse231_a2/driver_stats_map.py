#!/usr/bin/env python3

# Imports
import sys
import datetime as dt

# Constants
HEADER_KEYWORD = "medallion"
HACK_LICENSE_INDEX = 1
PICKUP_DATETIME_INDEX = 5
DROPOFF_DATETIME_INDEX = 6
TRIP_TIME_IN_SECS_INDEX = 8
PASSENGER_COUNT_INDEX = 7
TRIP_DISTANCE_INDEX = 9
TOTAL_AMOUNT_INDEX = 20

def determine_input_type(line):
    """Function to skip header in input data"""
    if (line.startswith(HEADER_KEYWORD)):
        return("header")
    else:
        return "valid"


def hours_covered(pickup_datetime, dropoff_datetime):
    """Function to determine if a trip spanned over multiple hours"""
    pickup_dt = dt.datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    dropoff_dt = dt.datetime.strptime(dropoff_datetime, "%Y-%m-%d %H:%M:%S")
    return dropoff_dt.hour - pickup_dt.hour
    

def get_key(split_line):
    """
    Finds individual key for a given driver/hour of specific day
    NOTE: Unique key created for a given driver driving during a given hour throughout a day. 
    Actual key is composed of ["hack"_"year"], but what is passed is ["hack"_"year"    "year-month-day hour"].
    """
    key = split_line[HACK_LICENSE_INDEX] + "_" + split_line[PICKUP_DATETIME_INDEX][0:4] + "\t" + split_line[PICKUP_DATETIME_INDEX][0:13]
    return key


def split_trip(split_line, total_time_of_trip, total_distance_of_trip, total_fare_of_trip, total_time_handled, first_line):
    """
    Will iteratively split a long trip into small trips that span individual hours, returning each on their own new line
    NOTE: This could probably be broken up more/be made more efficient, but we can cross that bridge if we need to/have time
    """
    pickup_dt = dt.datetime.strptime(split_line[PICKUP_DATETIME_INDEX], "%Y-%m-%d %H:%M:%S")
    dropoff_dt = dt.datetime.strptime(split_line[DROPOFF_DATETIME_INDEX], "%Y-%m-%d %H:%M:%S")
    
    # Handles case if it is the first segment of a long trip
    if first_line:
        
        # Updates dropoff time to keep it within the same hour as the pickup 
        split_line[DROPOFF_DATETIME_INDEX] = str(pickup_dt.replace(microsecond=0,second=0,minute=0) + dt.timedelta(hours = 1))
        
        # Calculates the duration of leg of trip
        split_line[TRIP_TIME_IN_SECS_INDEX] = str(int(((pickup_dt.replace(microsecond=0,second=0,minute=0) + dt.timedelta(hours = 1)) - pickup_dt).total_seconds()))
        
        # Calculates the fraction of trip this leg encompasses
        prop_of_trip = str(int(split_line[TRIP_TIME_IN_SECS_INDEX])/int(total_time_of_trip))
        
        # Calculates the trip leg distance
        trip_leg_distance = '%.3f' % (float(prop_of_trip) * float(total_distance_of_trip))
        split_line[TRIP_DISTANCE_INDEX] = str(trip_leg_distance)

        # Calculate the total fare amount for trip leg
        trip_leg_fare = '%.3f' % (float(prop_of_trip) * float(total_fare_of_trip))
        split_line[TOTAL_AMOUNT_INDEX] = str(trip_leg_fare)
        

        total_time_handled += int(split_line[TRIP_TIME_IN_SECS_INDEX])
        return split_line, total_time_handled
    
    # Handles following segments of a trip; major differences are in the handling of pickup and dropoff times
    else:
        
        # Eliminates passengers in the data, as they were not picked up during these intermediary segments
        split_line[PASSENGER_COUNT_INDEX] = str(0)
        
        # Updates pickup time to reflect new trip segment
        split_line[PICKUP_DATETIME_INDEX] = str(dropoff_dt)
        
        # Determine how much time is in this leg of trip; max of remaining time and 3600 seconds (i.e. one hour); allows for handling of multi-hour trips
        time_in_leg = min(3600, (int(total_time_of_trip) - total_time_handled))
        
        # Updates dropoff time to keep it within the same hour as the pickup
        split_line[DROPOFF_DATETIME_INDEX] = str(dt.datetime.strptime(split_line[PICKUP_DATETIME_INDEX], "%Y-%m-%d %H:%M:%S") + dt.timedelta(seconds = time_in_leg))
        
        # Calculates the duration of leg of trip
        split_line[TRIP_TIME_IN_SECS_INDEX] = str(time_in_leg)
        
        # Calculates the fraction of trip this leg encompasses
        prop_of_trip = str(int(split_line[TRIP_TIME_IN_SECS_INDEX])/int(total_time_of_trip))
        
        # Calculates the trip leg distance
        trip_leg_distance = '%.3f' % (float(prop_of_trip) * float(total_distance_of_trip))
        split_line[TRIP_DISTANCE_INDEX] = str(trip_leg_distance)

        # Calculate the total fare amount for trip leg
        trip_leg_fare = '%.3f' % (float(prop_of_trip) * float(total_fare_of_trip))
        split_line[TOTAL_AMOUNT_INDEX] = str(trip_leg_fare)
        
        total_time_handled += int(split_line[TRIP_TIME_IN_SECS_INDEX])
        return split_line, total_time_handled

    
def main():
    """ Map rows by using 'hack_license_year,pickup_hour' as key """
    for line in sys.stdin:
        split_line = line.split(",")
        
        # Handles header and collects information about the whole trip prior to manipulation in "split_trip"
        if (determine_input_type(line) == "valid"):
            trip_hours = hours_covered(split_line[PICKUP_DATETIME_INDEX], split_line[DROPOFF_DATETIME_INDEX])
            total_time_of_trip = split_line[TRIP_TIME_IN_SECS_INDEX]
            total_distance_of_trip = split_line[TRIP_DISTANCE_INDEX]
            total_fare_of_trip = split_line[TOTAL_AMOUNT_INDEX]
            total_time_handled = 0
            
            # Determines if the trip spanned one hour or multiple and prints the relevant number of lines
            if (trip_hours < 1):
                print(get_key(split_line) + "\t" + line, end = "")
            else:
                
                # Prints a unique line for each partition (i.e. hour) of the trip
                for i in range(trip_hours + 1):
                    first_line = True if (i == 0) else False
                    split_line, total_time_handled = split_trip(split_line, total_time_of_trip, total_distance_of_trip, total_fare_of_trip, total_time_handled, first_line)
                    print_line = ','.join(map(str, split_line))
                    
                    print(get_key(split_line) + "\t" + print_line)

    
if __name__ == "__main__":
    main()
