import re

increasing_regex = re.compile(r"^1*2*3*4*5*6*7*8*9*$")
has_pairs_regex = re.compile(r".*(.)\1.*")


def count_combinations(start, end):
    # Build a sequence of all values in range, as strings
    vals = range(start, end + 1)
    combinations = map(str, vals)

    # Enforce increasing values
    combinations = filter(increasing_regex.match, combinations)

    # Enforce at least 1 repeated digit
    combinations = filter(has_pairs_regex.match, combinations)

    # Count all matching combinations
    return sum(1 for c in combinations)


with open("data.txt", "r") as fp:
    start, end = map(int, fp.readline().split("-"))
    print(start, end)

print(count_combinations(start, end))
