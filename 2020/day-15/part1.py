from itertools import islice


def count(start=0, step=1):
    i = start
    while True:
        yield i
        i += step


def memory_game(starts):
    memory = {}

    isNew = True
    for i, val in enumerate(starts):
        yield val
        isNew = val not in memory
        memory[val] = i

    prev = val
    for i in count(start=i + 1):
        if isNew:
            val = 0
        else:
            val = i - memory[prev] - 1

        yield val
        isNew = val not in memory
        memory[prev] = i - 1
        prev = val


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    v = next(islice(iterable, n, None), default)
    print(v)
    return v


print(list(islice(memory_game([0, 3, 6]), 10)))
assert list(islice(memory_game([0, 3, 6]), 10)) == [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]
assert nth(memory_game([0, 3, 6]), 4) == 0
assert nth(memory_game([1, 3, 2]), 2020) == 1
assert nth(memory_game([2, 1, 3]), 2020) == 10
assert nth(memory_game([1, 2, 3]), 2020) == 27
assert nth(memory_game([2, 3, 1]), 2020) == 78
assert nth(memory_game([3, 2, 1]), 2020) == 438
assert (
    nth(
        memory_game(
            [
                3,
                1,
                2,
            ]
        ),
        2020,
    )
    == 1836
)
