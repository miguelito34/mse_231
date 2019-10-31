#!/usr/bin/env python3

from itertools import groupby
from operator import itemgetter
import sys
import datetime as dt
import numpy as np
import math

# Index used to separate fields in "fare" data that are and are not already in "trip" data.
FARE_DUPLICATE_FIELDS_INDEX = 5

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

# Function to return generator for key-value pairs in mapper/sort input
def read_mapper_output(input_stream, separator='\t'):
	for line in input_stream:
		yield line.rstrip().split(separator, 1)

# Function to correct or drop erroneous rows in joined dataset before printing to stdout
def perform_checks_and_cleaning(joined_list):
	# Drop rows that have zeroes for long/lat, distance, or time. Also drop rows with missing long/lat as this is needed for later checks.
	if ((joined_list[PICKUP_LONGITUDE_INDEX] == 0) or 
		(joined_list[PICKUP_LATITUDE_INDEX] == 0) or 
		(joined_list[DROPOFF_LONGITUDE_INDEX] == 0) or 
		(joined_list[DROPOFF_LATITUDE_INDEX] == 0) or 
		(joined_list[PICKUP_DATETIME_INDEX] == joined_list[DROPOFF_DATETIME_INDEX]) or 
		(joined_list[TRIP_DISTANCE_INDEX] == 0) or
		(joined_list[PICKUP_LONGITUDE_INDEX] == "") or
		(joined_list[PICKUP_LATITUDE_INDEX] == "") or
		(joined_list[DROPOFF_LONGITUDE_INDEX] == "") or
		(joined_list[DROPOFF_LATITUDE_INDEX] == "") 
	):
		return(False)
	else:
		# Drop rows where trip_distance < Euclidean distance between pickup & dropoff locations
		if (float(joined_list[TRIP_DISTANCE_INDEX]) < calc_distance(joined_list[PICKUP_LONGITUDE_INDEX], joined_list[PICKUP_LATITUDE_INDEX], joined_list[DROPOFF_LONGITUDE_INDEX], joined_list[DROPOFF_LATITUDE_INDEX])):
			return(False)
		else:
			return(True)

# Function to calculate trip time in seconds via pickup & dropoff times (more reliable), return as string
def reset_trip_time_in_secs(pickup_datetime, dropoff_datetime):
	pickup = dt.datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
	dropoff = dt.datetime.strptime(dropoff_datetime, "%Y-%m-%d %H:%M:%S")
	return(str(int((dropoff - pickup).total_seconds())))

# Calculate the distance between to locations
def calc_distance(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude):
	return(math.sqrt((float(pickup_longitude) - float(dropoff_longitude))**2 + (float(pickup_latitude) - float(dropoff_latitude))**2))


def main(separator='\t'):
	# Print joined header (trip + fare extra fields)
	print("medallion, hack_license, vendor_id, rate_code, store_and_fwd_flag, pickup_datetime, dropoff_datetime, passenger_count, trip_time_in_secs, trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, payment_type, fare_amount, surcharge, mta_tax, tip_amount, tolls_amount, total_amount")
	data = read_mapper_output(sys.stdin, separator = separator)
	for key, group in groupby(data, itemgetter(0)): 
		split_entry_trip = []
		split_entry_fare = []
		for entry in group:
			# Get either trip or fare data
			value = entry[1]
			if (value.startswith("trip")):
				split_entry_trip = value.split(",")
				del split_entry_trip[0] # Remove "trip" tag
			if (value.startswith("fare")):
				split_entry_fare = value.split(",")
				del split_entry_fare[:FARE_DUPLICATE_FIELDS_INDEX] # Remove "fare" tag
		# Join the unique fields
		joined_list = split_entry_trip + split_entry_fare
		# Process through checks in cleaning to determine what/if to print 
		if (perform_checks_and_cleaning(joined_list)):
			# Correct trip_time_in_secs via pickup & dropoff times (more reliable)
			reset_time = reset_trip_time_in_secs(joined_list[PICKUP_DATETIME_INDEX], joined_list[DROPOFF_DATETIME_INDEX])
			if (joined_list[TRIP_TIME_IN_SECS_INDEX] != reset_time):
				joined_list[TRIP_TIME_IN_SECS_INDEX] = reset_time
			print(",".join(joined_list))

if __name__ == "__main__":
	main()
