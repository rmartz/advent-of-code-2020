from functools import reduce
from collections import namedtuple, Counter, defaultdict
from itertools import chain
from math import ceil, gcd

BusSchedule = namedtuple("BusSchedule", ["offset", "interval"])


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


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


def history(items):
    for i, val in enumerate(items):
        yield items[:i], val


def lcm(nums):
    nums = list(nums)

    factors = defaultdict(int)
    for num in nums:
        counts = Counter(prime_factors(num))
        for p, count in counts.items():
            factors[p] = max(factors[p], count)

    return product(p ** count for p, count in factors.items())


def is_schedule_aligned(schedule, t, alignment):
    return (t + schedule.offset) % schedule.interval == 0


def find_next_alignment(target, start, step, alignment):
    if gcd(step, target.interval) != 1:
        raise Exception("Intervals are not relatively prime")
    for t in range(start, start + step * (target.interval + 1) + 1, step):
        if is_schedule_aligned(target, t, alignment):
            return t
    else:
        raise Exception("No solution found")


def find_soonest_alignment(ids):
    schedules = [
        BusSchedule(offset=offset, interval=int(interval))
        for offset, interval in enumerate(ids)
        if interval != "x"
    ]

    alignment = schedules[0].interval

    # The solution requires all buses to be aligned with their offset
    # Find buses that are aligned, and increment such that they will remain aligned
    #   while we attempt to align with more buses.
    # Start with the slowest bus, and increment by that bus's interval
    # If a 60 minute bus with offset 10 works at 70 minutes, and also at 130 minutes
    # When we align with other buses, we step by the LCM of all found bus intervals
    # e.g., if a 6 minute and 9 minute bus are aligned, they will be aligned again
    #   exactly every 18 minutes
    t = 0

    for fits, target in history(schedules):
        step = lcm(schedule.interval for schedule in fits)
        t = t % step

        t = find_next_alignment(target, t, step, alignment)

    return t


assert lcm([3, 9]) == 9
assert lcm([3, 5]) == 15
assert lcm([4, 78, 43, 13, 8, 25]) == 335400
assert find_soonest_alignment("7,13,x,x,59,x,31,19".split(",")) == 1068781
assert find_soonest_alignment("17,x,13,19".split(",")) == 3417
assert find_soonest_alignment("67,7,59,61".split(",")) == 754018
assert find_soonest_alignment("67,x,7,59,61".split(",")) == 779210
assert find_soonest_alignment("67,7,x,59,61".split(",")) == 1261476
assert find_soonest_alignment("1789,37,47,1889".split(",")) == 1202161486

print("Tests passed, running on input...")

with open("./data.txt", "r") as fp:
    _, bus_ids = fp.readlines()

ids = bus_ids.split(",")

print(find_soonest_alignment(ids))
