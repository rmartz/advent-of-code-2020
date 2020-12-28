from operator import itemgetter
from itertools import islice
from functools import reduce


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


def circular_extract(lst, start, stop):
    start %= len(lst)
    stop %= len(lst)
    if stop < start:
        # We loop around, and want to grab the inside of the list
        return lst[stop:start], lst[start:] + lst[:stop]
    return lst[:start] + lst[stop:], lst[start:stop]


def circular_insert(lst, pos, vals):
    pos %= len(lst)

    return lst[:pos] + vals + lst[pos:]


def circular_center_on_pos(lst, pos):
    # Re-adjust the list so that pos is index 0
    return lst[pos:] + lst[:pos]


def find_destination_cup(lst, start_val):
    positions = list(enumerate(lst))
    try:
        smaller_vals = [item for item in positions if item[1] < start_val]
        pos, _ = max(smaller_vals, key=itemgetter(1))
    except ValueError:
        pos, _ = max(positions, key=itemgetter(1))
    return pos


def shuffle_cups(lst):
    pos = 0
    while True:
        yield lst

        pos %= len(lst)
        start_val = lst[pos]

        lst, picked_up = circular_extract(lst, pos + 1, pos + 4)
        destination = find_destination_cup(lst, start_val)

        lst = circular_insert(lst, destination + 1, picked_up)

        pos = lst.index(start_val) + 1


def expand_cups(lst):
    return lst + list(range(max(lst)+1, 1000001))


def find_adjacent_cups(lst):
    pos = lst.index(1)
    return (
        lst[(pos + 1) % len(lst)],
        lst[(pos + 2) % len(lst)]
    )


def progress_printer(it, interval):
    for i, v in enumerate(it):
        if i % interval == 0:
            print(i)
        yield v


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    v = next(islice(iterable, n, None), default)
    return v


assert circular_extract([1, 2, 3], 1, 2) == ([1, 3], [2])
assert circular_extract([1, 2, 3], 2, 4) == ([2], [3, 1])

assert circular_insert([1, 2], 1, [99]) == [1, 99, 2]

assert find_destination_cup([1, 2, 3, 4], 2) == 0
assert find_destination_cup([1, 2, 3, 4], 0) == 3


with open("./data.txt", "r") as fp:
    vals = [int(v) for v in fp.read().strip()]

vals = expand_cups(vals)

states = progress_printer(shuffle_cups(vals), 1000)
final_state = nth(states, 10000000)

target_cups = find_adjacent_cups(final_state)
print(target_cups)
print(product(target_cups))
