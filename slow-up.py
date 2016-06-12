#!/usr/bin/python3

import getopt
import re
import sys
import os
from datetime import datetime
from datetime import timedelta

# handling parameters
try:
    options, arguments = getopt.gnu_getopt(sys.argv[1:], "o:h:m:s:f:")
except getopt.GetoptError as err:
    print("Illegal arguments")
    print(err)
    sys.exit(1)

if len(arguments) < 1:
    print("No input file, abort.")
    sys.exit(1)

input_name = arguments[0]

# get options passed
mode = "fast"
times = { "hours" : 0, "minutes" : 0, "seconds": 0, "microseconds": 0 }
for option, argument in options:
    if option == "-h":
        times["hours"] = int(argument)
    if option == "-m":
        times["minutes"] = int(argument)
    if option == "-s":
        times["seconds"] = int(argument)
    if option == "-f":
        times["microseconds"] = int(argument)
    if option == "-o":
        mode = argument

factor = 1
if mode == "fast":
    factor = -factor

# regex for extracting times
pattern = "([0-9:,]+) --> ([0-9:,]+)"
matcher = re.compile(pattern)

# reading files
with open(input_name) as file:
    content = file.readlines()

# chosing a file name with a default value
if len(arguments) > 1:
    output_name = arguments[1]
else:
    output_name = os.path.basename(input_name)[:-4] + "_slow-up.srt"

# writing to file
out_file = open(output_name, 'w')

# extracting timestamps from each line
time_format = "%H:%M:%S,%f"

# creating delta with passed in options
delta = timedelta(hours = times["hours"] * factor, 
        minutes = times["minutes"] * factor, 
        seconds = times["seconds"] * factor, 
        microseconds = times["microseconds"] * factor)

for line in content:
    times = matcher.match(line)
    if times:
        # turn strings into date times
        start_date = datetime.strptime(times.group(1), time_format)
        end_date = datetime.strptime(times.group(2), time_format)

        # adjust time using timedelta
        start_edit = start_date + delta
        end_edit = end_date + delta

        # convert date time back to strings
        start_format = start_edit.strftime(time_format)[:-3]
        end_format = end_edit.strftime(time_format)[:-3]

        # write strings in srt format
        out_file.write(start_format + " --> " + end_format + "\n")
    else:
        out_file.write(line)

out_file.close()
