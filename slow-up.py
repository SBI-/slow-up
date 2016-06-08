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

# extracting timestamps from each line
for line in content:
    times = matcher.match(line)
    if times:
        start = datetime.strptime(times.group(1), "%H:%M:%S,%f")
        end = datetime.strptime(times.group(2), "%H:%M:%S,%f")
