from collections import namedtuple, defaultdict, Counter
from itertools import groupby
from functools import reduce

Tile = namedtuple("Tile", ["id", "edges"])


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


def get_edges(raw):
    return (
        raw[0],
        raw[-1],
        ''.join(line[0] for line in raw),
        ''.join(line[-1] for line in raw)
    )


def load_tile(lines):
    label = next(lines)
    raw = list(lines)

    return Tile(
        # The label is always formatted as "Tile {id}:"
        id=int(str(label[5:-1])),
        edges=get_edges(raw)
    )


with open("./data.txt", "r") as fp:
    lines = (line.strip() for line in fp)
    groups = groupby(lines, lambda line: line == "")

    raw_tiles = (group for is_blank, group in groups if not is_blank)

    all_tiles = set(load_tile(tile) for tile in raw_tiles)

# Find all edges that match with another tile
edges = defaultdict(list)
for tile in all_tiles:
    for edge in tile.edges:
        assert type(edge) == str
        if edge not in edges:
            edge = edge[::-1]
        edges[edge].append(tile)

# Verify that all edges found a single unique match
# If each edge just has a single match, we can assume that they are matched without
# having to consider the actual puzzle's geometry.
assert max(len(tiles) for tiles in edges.values()) == 2

# Outside edges are any edge that doesn't have a match
outside_edges = [tiles[0].id for tiles in edges.values() if len(tiles) == 1]

# Corners are the same tile with two outside edges
corner_tile_ids = [tile for tile, count in Counter(outside_edges).items() if count == 2]
assert len(corner_tile_ids) == 4
print(product(corner_tile_ids))
