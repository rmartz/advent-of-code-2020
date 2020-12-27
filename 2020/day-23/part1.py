from operator import itemgetter
from itertools import islice


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


def render_cups(lst):
    # Center on 1
    center = lst.index(1)
    lst = circular_center_on_pos(lst, center)
    # Remove the fixed center value
    lst = lst[1:]
    return "".join(str(v) for v in lst)


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    v = next(islice(iterable, n, None), default)
    return v


assert circular_extract([1, 2, 3], 1, 2) == ([1, 3], [2])
assert circular_extract([1, 2, 3], 2, 4) == ([2], [3, 1])

assert circular_insert([1, 2], 1, [99]) == [1, 99, 2]

assert find_destination_cup([1, 2, 3, 4], 2) == 0
assert find_destination_cup([1, 2, 3, 4], 0) == 3


assert render_cups(nth(shuffle_cups([3, 8, 9, 1, 2, 5, 4, 6, 7]), 10)) == "92658374"
assert render_cups(nth(shuffle_cups([3, 8, 9, 1, 2, 5, 4, 6, 7]), 100)) == "67384529"


with open("./data.txt", "r") as fp:
    vals = [int(v) for v in fp.read().strip()]


final_state = nth(shuffle_cups(vals), 100)
print(render_cups(final_state))
