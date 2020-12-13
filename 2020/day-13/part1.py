from functools import reduce


def wait_next_arrival(time, schedule):
    return schedule - (time % schedule)


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


with open("./data.txt", "r") as fp:
    time, bus_ids = fp.readlines()

    time = int(time)
    bus_ids = (int(id) for id in bus_ids.split(",") if id != "x")

    pairs = ((id, wait_next_arrival(time, id)) for id in bus_ids)

    next_arrival = min(pairs, key=lambda tup: tup[1])
    print(product(next_arrival))
