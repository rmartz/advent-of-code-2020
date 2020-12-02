from collections import defaultdict
from operator import itemgetter
from itertools import groupby
import re

guard_shift_re = re.compile('.*Guard #(\d+) begins shift')
def guard_tracker(records):
    guard = None
    for record in records:
        shift_check = guard_shift_re.match(record)
        if shift_check:
            guard = int(shift_check.group(1))
        yield (guard, record)

def guard_intervals(shifts):
    print(shifts)
    for records in shifts:
        record_times = (record[1:17] for record in records)
        prev = next(record_times)
        awake = True
        for cur in record_times:
            yield ((prev, cur), awake)
            prev = cur
            awake = not awake

def record_minutes(time):
    return int(time[14:16])


with open('data.txt', 'r') as fp:
    records = sorted(fp)


guard_records = defaultdict(list)
for guard, records in groupby(guard_tracker(records), itemgetter(0)):
    records = map(itemgetter(1), records)
    guard_records[guard] += [list(records)]

sleepiest_guard = (0, (0, 0))
for guard, records in guard_records.items():
    print('-----')
    intervals = guard_intervals(records)
    sleeping_times = [interval for interval, awake in intervals if not awake]
    if not sleeping_times:
        continue
    print(sleeping_times)

    sleeping_minutes = [map(record_minutes, times) for times in sleeping_times]

    time_sleeping = sum(end - start - 1 for start, end in sleeping_minutes)

    if time_sleeping > sleepiest_guard[0]:
        times_slept = defaultdict(int)
        for start, end in sleeping_minutes:
            for m in range(start, end):
                times_slept[m] += 1
        print(times_slept)
        most_times_slept = max(times_slept.items(), key=itemgetter(1))
        sleepiest_minute = most_times_slept[0]
        print(sleepiest_minute)

        sleepiest_guard = (time_sleeping, (guard, sleepiest_minute))
        print(sleepiest_guard)


print(sleepiest_guard[1][0] * sleepiest_guard[1][1])