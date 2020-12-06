from itertools import groupby
import re

increasing_regex = re.compile(r"^1*2*3*4*5*6*7*8*9*$")


def check_explicit_pair(c):
    group_lengths = (sum(1 for v in vals) for char, vals in groupby(c))
    return any(length == 2 for length in group_lengths)


def count_combinations(start, end):
    # Build a sequence of all values in range, as strings
    vals = range(start, end + 1)
    combinations = map(str, vals)

    # Enforce increasing values
    combinations = filter(increasing_regex.match, combinations)

    # Enforce at least 1 repeated digit
    combinations = filter(check_explicit_pair, combinations)

    # Count all matching combinations
    return sum(1 for c in combinations)


assert count_combinations(223450, 223450) == 0
assert count_combinations(112233, 112233) == 1
assert count_combinations(122334, 122334) == 1
assert count_combinations(123444, 123444) == 0
assert count_combinations(124444, 124444) == 0
assert count_combinations(111122, 111122) == 1

with open("data.txt", "r") as fp:
    start, end = map(int, fp.readline().split("-"))
    print(start, end)

print(count_combinations(start, end))
