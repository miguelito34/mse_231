#!/usr/bin/env python3

# Imports
import sys

# Constants
HEADER_KEYWORD = "medallion"
NUM_COMMAS_TRIP = 13
NUM_COMMAS_FARE = 10
HACK_LICENSE_INDEX_TRIP = 1
PICKUP_DATETIME_INDEX_TRIP = 5
HACK_LICENSE_INDEX_FARE = 1
PICKUP_DATETIME_INDEX_FARE = 3
ERROR_MESSAGE = "ERROR"
KEY_VALUE_SEPARATOR = "\t"

def determine_input_type(line):
	"""Function to determine which data table line comes from or if it is a header"""
	if (line.startswith(HEADER_KEYWORD)):
		return("header")
	else:
		num_commas = line.count(',')
		if (num_commas == NUM_COMMAS_TRIP):
			return("trip")
		elif (num_commas == NUM_COMMAS_FARE):
			return("fare")
		else:
			return(ERROR_MESSAGE)

def get_key(line, input_type):
	"""Function to create and return a key for mapping the given line"""
	key = ""
	split_line = line.split(',')
	if (input_type == "trip"):
		key = str(split_line[HACK_LICENSE_INDEX_TRIP]) + "," + str(split_line[PICKUP_DATETIME_INDEX_TRIP])
	elif (input_type == "fare"):
		key = str(split_line[HACK_LICENSE_INDEX_FARE]) + "," + str(split_line[PICKUP_DATETIME_INDEX_FARE])
	return key

def main():
	for line in sys.stdin:
		input_type = determine_input_type(line)
		# Print line if it is not a header and the input type was properly identified
		if (input_type != "header" and input_type != ERROR_MESSAGE):
			print(get_key(line, input_type) + KEY_VALUE_SEPARATOR + input_type + "," + line, end = "")

if __name__ == "__main__":
	main()
