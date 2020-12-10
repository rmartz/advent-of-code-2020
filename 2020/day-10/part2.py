from itertools import groupby
from functools import reduce


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


def differences(seq, start):
    prev = start
    for val in seq:
        yield val - prev
        prev = val
    yield 3


def count_arrangements(seq):
    # Only arrangements revolve around removing optional stages
    # Any gap of 3 is at max size, so requires both sides
    # We can use that to break the sequence into blocks, and multiply those
    blocks = (
        count_block_arrangements(block)
        for isGap, block in groupby(seq, lambda diff: diff == 3)
        if not isGap
    )
    return product(blocks)


def count_block_arrangements(block):
    # Possible replacements:
    # 1 1 -> 2
    # 2 1 -> 3
    # 1 2 -> 3
    block = list(block)
    acc = 1
    for i in range(len(block) - 1):
        a, b, *rem = block[i:]
        if a + b <= 3:
            acc += count_block_arrangements([a + b] + rem)
    return acc


with open("./data.txt", "r") as fp:
    vals = sorted(int(val) for val in fp)
    diffs = differences(vals, 0)
    print(count_arrangements(diffs))
