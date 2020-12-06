from collections import Counter

INDEXES = (2, 3)


def count_instances(row):
    counts = Counter(row).values()
    return [any(count == val for count in counts) for val in INDEXES]


with open("data.txt", "r") as fp:
    matches = list(count_instances(row) for row in fp)
    counts = [sum(1 if v else 0 for v in col) for col in zip(*matches)]
    print(counts[0] * counts[1])
