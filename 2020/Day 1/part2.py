from itertools import combinations
from functools import reduce


def product(*args):
    return reduce(lambda val, acc: val * acc, args, 1)


def find_sum(data, count, target):
    for triple in combinations(data, count):
        if sum(triple) == target:
            return triple
    raise Exception("No matching values were found")


with open('./data.txt', 'r') as fp:
    data = [int(line) for line in fp.readlines()]

values = find_sum(data, 3, 2020)
print(product(*values))
