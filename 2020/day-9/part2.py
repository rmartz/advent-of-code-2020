import itertools


# Class for creating "probe" sub-iterators that can peek ahead
class IterProbe(object):
    seq = None
    history = None

    def __init__(self, seq):
        self.history = []
        self.seq = iter(seq)

    def probe(self):
        yield from self.history
        for val in self.seq:
            self.history.append(val)
            yield val

    def advance(self):
        if self.history:
            self.history.pop(0)
        else:
            next(self.seq)


def history(seq, max_size):
    it = iter(seq)
    prev = []
    # prev is growing until we reach max_size items, we can just append each item
    for val in itertools.islice(it, max_size):
        yield prev, val
        prev.append(val)

    # Now that prev has max_size items in it, pop an item before adding the next
    for val in it:
        yield prev, val
        prev.pop(0)
        prev.append(val)


def find_sum(data, target):
    high = len(data) - 1
    low = 0
    while high >= low:
        high_val = data[high]
        low_val = data[low]
        total = high_val + low_val
        if total == target:
            return high_val, low_val
        elif total < target:
            # Need to increase the total
            # Because every low number can pair with exactly one high number,
            # if the value is too low then there is no matching high number
            low += 1
        else:
            # Need to decrease the total
            # Similarly, if the value is too high then there is no matching
            #  low number. Use the next high to see how it fairs
            high -= 1
    raise Exception("Target was not found")


def find_invalid(stream, lookback_len, preamble_len):
    # Keep the previous lookback as we iterate through
    stream = history(vals, lookback_len)

    # Truncate the preamble since we are not validating that
    stream = itertools.islice(stream, preamble_len, None)

    for prev, target in stream:
        data = sorted(prev)
        try:
            find_sum(data, target)
        except Exception:
            # No two numbers in the previous
            return target


def get_contiguous_set_with_sum(vals, target):
    total = 0
    for val in vals:
        total += val
        if total > target:
            raise Exception("Set does not total to sum")
        yield val
        if total == target:
            return


def find_contiguous_set_with_sum(vals, target):
    it = IterProbe(vals)

    while True:
        try:
            probe = it.probe()
            return list(get_contiguous_set_with_sum(probe, target))
        except Exception:
            it.advance()


def find_min_max(numbers):
    it = iter(numbers)
    low = high = next(it)
    for n in it:
        low = min(low, n)
        high = max(high, n)

    return (low, high)


TARGET = 1930745883

with open("./data.txt", "r") as fp:
    vals = (int(val) for val in fp)
    contiguous_set = find_contiguous_set_with_sum(vals, TARGET)
    min_max = find_min_max(contiguous_set)

    print(sum(min_max))

