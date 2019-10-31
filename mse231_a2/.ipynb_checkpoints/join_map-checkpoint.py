#!/usr/bin/env python3

import sys

HEADER_KEYWORD = "medallion"
NUM_COMMAS_TRIP = 13
NUM_COMMAS_FARE = 10
HACK_LICENSE_INDEX_TRIP = 1
PICKUP_DATETIME_INDEX_TRIP = 5
HACK_LICENSE_INDEX_FARE = 1
PICKUP_DATETIME_INDEX_FARE = 3

def determine_input_type(line):
	if (line.startswith(HEADER_KEYWORD)):
		return("header")
	else:
		num_commas = line.count(',')
		if (num_commas == NUM_COMMAS_TRIP):
			return("trip")
		elif (num_commas == NUM_COMMAS_FARE):
			return("fare")
		else:
			return("ERROR_input_type")

def get_key(line, input_type):
	key = ""
	split_line = line.split(',')
	if (input_type == "trip"):
		key = str(split_line[HACK_LICENSE_INDEX_TRIP]) + "," + str(split_line[PICKUP_DATETIME_INDEX_TRIP])
	elif (input_type == "fare"):
		key = str(split_line[HACK_LICENSE_INDEX_FARE]) + "," + str(split_line[PICKUP_DATETIME_INDEX_FARE])
	else:
		key = "ERROR_get_key()"
	return key

def main():
	""" Map rows by using 'hack_license,pickup_datetime' as key"""
	for line in sys.stdin:
		input_type = determine_input_type(line)
		if (input_type != "header" and input_type != "ERROR_input_type"):
			print(get_key(line, input_type) + "\t" + input_type + "," + line, end = "")

if __name__ == "__main__":
    main()
