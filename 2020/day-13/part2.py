from functools import reduce


def count(start=0, step=1):
    i = start
    while True:
        yield i
        i += step


def wait_next_arrival(time, schedule):
    return schedule - (time % schedule)


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


def buses_arrive_consecutive_minutes(t, bus_pairs):
    for id, index in bus_ids:
        if wait_next_arrival(t, id) != index:
            return False
    return True


with open("./data.txt", "r") as fp:
    _, bus_ids = fp.readlines()

    bus_ids = [(int(id), index) for index, id in enumerate(bus_ids.split(',')) if id != 'x']
    step = bus_ids[0][1]

    for t in count(start=step, step=step):
        if buses_arrive_consecutive_minutes(t, bus_ids):
            print(t)
            break

