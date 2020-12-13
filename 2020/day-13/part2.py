from functools import reduce
from collections import namedtuple, Counter, defaultdict
from itertools import chain

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
    return schedule - (time % schedule)


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


def buses_arrive_on_consecutive_minutes(t, schedules):
    for schedule in schedules:
        wait_until = wait_next_arrival(t, schedule.interval)
        if wait_until == schedule.offset:
            yield schedule


assert lcm([3, 9]) == 9
assert lcm([3, 5]) == 15
assert lcm([4, 78, 43, 13, 8, 25]) == 335400


with open("./data.txt", "r") as fp:
    _, bus_ids = fp.readlines()

ids = bus_ids.split(',')

schedules = set(BusSchedule(offset=offset, interval=int(interval)) for offset, interval in enumerate(ids) if interval != 'x')

slowest = min(schedules, key=lambda schedule: schedule.interval)

# The solution requires all buses to be aligned with their offset
# Find buses that are aligned, and increment such that they will remain aligned while
#   we attempt to align with more buses.
# Start with the slowest bus, and increment by that bus's interval
# If a 60 minute bus with offset 10 works at 70 minutes, and also at 130 minutes
# When we align with other buses, we step by the LCM of all found bus intervals
# e.g., if a 60 minute and 90 minute bus are aligned, they will be aligned precisely once every 180 minutes
t = slowest.offset
step = slowest.interval
fits = set([slowest])
remainder = schedules - fits
cycle_loop = lcm(schedule.interval for schedule in schedules)

while remainder:
    if t > cycle_loop * max(schedule.interval for schedule in remainder) * 1000:
        raise Exception("No solution found")
    t += step

    new_fits = set(buses_arrive_on_consecutive_minutes(t, remainder))
    if new_fits:
        fits |= new_fits
        remainder -= new_fits
        print(fits)
        print(remainder)
        step = lcm(schedule.interval for schedule in fits)
        t %= step
        print(step)


print(t % step)
