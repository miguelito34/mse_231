#!/usr/bin/env python3

# Imports
import sys

# Constants
HEADER_KEYWORD = "date"
DATE_INDEX = 0
HOUR_INDEX = 1
T_ONDUTY_INDEX = 3

def determine_input_type(line):
    """Function to skip header in input data"""
    if (line.startswith(HEADER_KEYWORD)):
        return("header")
    else:
        return "valid"

def get_key(split_line):
    """Function to get key for a given day"""
    return (str(split_line[DATE_INDEX]) + "," + str(split_line[HOUR_INDEX]))


def main():
    # Map rows by using 'date,year' as key
    for line in sys.stdin:
        split_line = line.split(",")
        
        # Maps hours in which drivers were on duty for at least 1 minute
        if (determine_input_type(line) == "valid" and float(split_line[T_ONDUTY_INDEX]) >= .0166):
            print(get_key(split_line) + "\t" + line)
          
        
if __name__ == "__main__":
    main()
