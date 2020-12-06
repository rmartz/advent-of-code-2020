from collections import defaultdict
from functools import lru_cache

relationships = defaultdict(list)


@lru_cache(maxsize=None)
def count_relationships(id):
    return len(relationships.get(id, [])) + sum(
        count_relationships(sub_id) for sub_id in relationships.get(id, [])
    )


def count_all_relationships():
    return sum(count_relationships(id) for id in relationships.keys())


with open("data.txt", "r") as fp:
    orbit_pairs = (line.strip().split(")") for line in fp)
    for target, satelite in orbit_pairs:
        relationships[target].append(satelite)

    print(count_all_relationships())
