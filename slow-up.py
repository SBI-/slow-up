#!/usr/bin/python3

import getopt
import re
from datetime import datetime

# bit about getting times
pattern = "([0-9:,]+) --> ([0-9:,]+)"
text = "02:04:40,724 --> 02:04:41,724"
matcher = re.compile(pattern)

# reading files
with open("../A.New.Hope.1977.Bluray.english.srt") as file:
    content = file.readlines()

# writing to file
out_file = open("output", 'w')

# extracting timestamps from each line
time_format = "%H:%M:%S,%f"

for line in content:
    times = matcher.match(line)
    if times:
        # turn strings into date times
        start_date = datetime.strptime(times.group(1), time_format)
        end_date = datetime.strptime(times.group(2), time_format)
        # adjust time using timedelta

        # convert date time back to strings
        start_format = start_date.strftime(time_format)[:-3]
        end_format = start_date.strftime(time_format)[:-3]
        # write strings in srt format
        out_file.write(start_format + " --> " + end_format + "\n")
    else:
        out_file.write(line)

out_file.close()
