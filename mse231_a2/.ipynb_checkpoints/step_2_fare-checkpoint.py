import sys

header = True
selected_day = "2013-01-01"
column_for_date = 3

for line in sys.stdin:
	if header:
		print(line, end = "")
		header = False
		continue
	split_line = line.split(',')
	date = split_line[column_for_date]
	if (date.startswith(selected_day)):
		print(line, end = "")
