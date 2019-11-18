#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
 
import sys
import re
import csv

census ={}

#dictionary of census data with the keys being geoid and values being the rest 
with open('census_data.tsv') as f:
	census_data = csv.reader(f, delimiter = '\t')
	for line in census_data:
		census[line[0]] = line[1:]

for line in sys.stdin:
	line = line.split("\t")
	line[10] = line[10].replace('\n', '')
	call_geoid = line[10]
	census_data = census[call_geoid]
	output = line + census_data
	print(*output, sep = "\t")

