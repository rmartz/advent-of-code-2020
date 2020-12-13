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


def aligned_times(schedule, cycle_repeat, alignment):
    for t in range(0, cycle_repeat+1, schedule.interval):
        if (schedule.interval - (t % alignment)) % schedule.interval == schedule.offset:
            yield t


def it_intersection(sets):
    it = iter(sets)
    intersection = set(next(it))
    for s in it:
        intersection &= set(s)
    return intersection


assert lcm([3, 9]) == 9
assert lcm([3, 5]) == 15
assert lcm([4, 78, 43, 13, 8, 25]) == 335400


with open("./data.txt", "r") as fp:
    _, bus_ids = fp.readlines()

ids = bus_ids.split(',')

schedules = [BusSchedule(offset=offset, interval=int(interval)) for offset, interval in enumerate(ids) if interval != 'x']

cycle_length = lcm(schedule.interval for schedule in schedules)


alignment = schedules[0].interval

for moment in range(0, cycle_length+1, alignment):
    if all(wait_next_arrival(moment, schedule.interval) == schedule.offset for schedule in schedules):
        print(moment)
        break
