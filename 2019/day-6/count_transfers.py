from collections import defaultdict
from functools import lru_cache

relationships = {}


def list_ancestors(id):
    while True:
        try:
            parent = relationships[id]
        except KeyError:
            return
        yield parent
        id = parent


def count_transfers(src, dst):
    src_ancestors = set(list_ancestors(src))
    dst_ancestors = set(list_ancestors(dst))

    common_ancestors = src_ancestors.intersection(dst_ancestors)

    return len(src_ancestors) + len(dst_ancestors) - 2 * len(common_ancestors)


with open("data.txt", "r") as fp:
    orbit_pairs = (line.strip().split(")") for line in fp)
    for target, satelite in orbit_pairs:
        relationships[satelite] = target

    print(count_transfers("YOU", "SAN"))
