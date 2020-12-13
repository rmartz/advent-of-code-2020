from functools import reduce
from collections import namedtuple, Counter, defaultdict
from itertools import chain
from math import ceil

BusSchedule = namedtuple("BusSchedule", ['offset', 'interval'])


def prime_factors(val):
    for p in chain([2], count(start=3, step=2)):
        while val % p == 0:
            yield p
            val //= p
        if val == 1:
            return


def count(start=0, step=1):
    i = start
    while True:
        yield i
        i += step


def wait_next_arrival(time, schedule):
    return (schedule - (time % schedule)) % schedule


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


def lcm(nums):
    nums = list(nums)

    factors = defaultdict(int)
    for num in nums:
        counts = Counter(prime_factors(num))
        for p, count in counts.items():
            factors[p] = max(factors[p], count)

    return product(p ** count for p, count in factors.items())


def next_aligned_time(schedule, cycle_repeat, alignment, start=0):
    # Make sure start is alligned with this schedule
    start = int(ceil(start / schedule.interval)) * schedule.interval
    for t in range(start, cycle_repeat+1, schedule.interval):
        if t % alignment == schedule.offset % alignment:
            return t - schedule.offset


def it_intersection(sets):
    it = iter(sets)
    intersection = set(next(it))
    for s in it:
        intersection &= set(s)
    return intersection


def find_soonest_alignment(ids):
    schedules = [BusSchedule(offset=offset, interval=int(interval)) for offset, interval in enumerate(ids) if interval != 'x']

    cycle_length = lcm(schedule.interval for schedule in schedules)

    alignment = schedules[0].interval

    # Store a dictionary of each schedule and the next aligned time that could be shared by all
    next_alignments = {
        schedule: next_aligned_time(schedule, cycle_length, alignment, 0)
        for schedule in schedules
    }

    # Find the soonest and latest possible alignments, and jump the soonest alignment to the next
    # time that happens at or after the current latest alignment
    # Eventually all schedules should share the same soonest alignment
    soonest_alignment = 0
    while soonest_alignment < cycle_length:
        soonest_schedule, soonest_alignment = min(next_alignments.items(), key=lambda pair: pair[1])
        latest = max(next_alignments.values())
        if soonest_alignment < latest:
            next_alignments[soonest_schedule] = next_aligned_time(soonest_schedule, cycle_length, alignment, latest)
        else:
            return soonest_alignment
    raise Exception("No solution found")


assert lcm([3, 9]) == 9
assert lcm([3, 5]) == 15
assert lcm([4, 78, 43, 13, 8, 25]) == 335400
assert find_soonest_alignment('7,13,x,x,59,x,31,19'.split(',')) == 1068781
assert find_soonest_alignment('17,x,13,19'.split(',')) == 3417
assert find_soonest_alignment('67,7,59,61'.split(',')) == 754018
assert find_soonest_alignment('67,x,7,59,61'.split(',')) == 779210
assert find_soonest_alignment('67,7,x,59,61'.split(',')) == 1261476
assert find_soonest_alignment('1789,37,47,1889'.split(',')) == 1202161486

print("Tests passed, running on input...")

with open("./data.txt", "r") as fp:
    _, bus_ids = fp.readlines()

ids = bus_ids.split(',')

print(find_soonest_alignment(ids))
