from collections import Counter


def differences(seq, start):
    prev = start
    for val in seq:
        yield val - prev
        prev = val
    yield 3


with open("./data.txt", "r") as fp:
    vals = sorted(int(val) for val in fp)
    diffs = differences(vals, 0)
    counts = Counter(diffs)
    print(counts[1] * counts[3])
