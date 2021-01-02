from collections import namedtuple, defaultdict, Counter
from itertools import groupby
from functools import reduce


Border = namedtuple("Border", ["north", "south", "east", "west"])


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


def remainder(lst):
    for i, val in enumerate(lst):
        yield val, lst[:i] + lst[i+1:]


def count(start=0, step=1):
    i = start
    while True:
        yield i
        i += step


def diagonalize():
    for step in count():
        for x in range(step):
            yield Vector(x=x, y=step-x)



Vector = namedtuple("Vector", ["x", "y"])


def add_vectors(a: Vector, b: Vector) -> Vector:
    return Vector(x=a.x + b.x, y=a.y + b.y)


ADJACENCIES = [
    Vector(x=x, y=y) for x in [-1, 0, 1] for y in [-1, 0, 1] if x != 0 or y != 0
]


def get_neighbors(node):
    for direction in ADJACENCIES:
        yield add_vectors(node, direction)


class Tile(object):
    id = None
    edges = None
    content = None

    @staticmethod
    def get_edges(raw):
        return Border(
            north=raw[0],
            south=raw[-1],
            east=''.join(line[-1] for line in raw),
            west=''.join(line[0] for line in raw),
        )

    @staticmethod
    def get_content(raw):
        for row in raw[1:-1]:
            yield row[1:-1]

    def __init__(self, id, raw):
        self.id = id
        self.edges = self.get_edges(raw)
        self.content = self.get_content(raw)

    def _flip_content_horizontally(self):
        self.content = [row[::-1] for row in self.content]

    def _flip_edges_horizontally(self):
        # Swap North to South
        self.edges = Border(
            north=self.edges.south,
            south=self.edges.north,
            east=tuple(self.edges.east[::-1]),
            west=tuple(self.edges.west[::-1]),
        )

    def flip_tile_horizontally(self):
        self._flip_content_horizontally()
        self._flip_edges_horizontally()

    def _flip_content_vertically(self):
        self.content = [row[:] for row in self.content[::-1]]

    def _flip_edges_vertically(self):
        # Swap East to West
        self.edges = Border(
            north=tuple(self.edges.north[::-1]),
            south=tuple(self.edges.south[::-1]),
            east=self.edges.west,
            west=self.edges.east,
        )

    def flip_tile_vertically(self):
        self._flip_content_vertically()
        self._flip_edges_vertically()

    def _rotate_content_clockwise(self):
        pass

    def rotate_tile_clockwise(tile):
        pass


def load_tile(lines):
    label = next(lines)
    raw = list(lines)

    return Tile(
        # The label is always formatted as "Tile {id}:"
        id=int(str(label[5:-1])),
        raw=raw
    )


def tiles_to_shared_edges(tiles):
    edges = defaultdict(list)
    for tile in tiles:
        for edge in tile.edges:
            assert type(edge) == str
            if edge not in edges:
                edge = edge[::-1]
            edges[edge].append(tile.id)

    # Verify that all edges found a single unique match
    # If each edge just has a single match, we can assume that they are matched without
    # having to consider the actual puzzle's geometry.
    assert max(len(tiles) for tiles in edges.values()) == 2

    return edges


def vertices_to_adjacency_lookup(vertices):
    # Convert a list of vertices into a dictionary of node and its neighbors
    # Vertexes are represented as a sequence of tuples/list of connected nodes
    neighbor_lookup = defaultdict(set)
    for vertex in vertices:
        for node, neighbors in remainder(vertex):
            print(neighbors)
            neighbor_lookup[node] |= set(neighbors)
    return neighbor_lookup


def adjacency_lookup_to_grid(lookup):
    edges = set(id for id, neighbors in lookup.items() if len(neighbors) <= 3)
    corners = set(id for id in edges if len(lookup[id]) == 2)

    # Find a corner arbitrarily and set it as (0, 0)
    # Pick one adjacency to be arbitrarily (1, 0)
    corner = list(corners)[0]
    grid = {
        Vector(x=0, y=0): corner,
        Vector(x=1, y=0): list(lookup[corner])[0]
    }

    placed_nodes = set(grid.values())

    # Place the first line left to right, using the edge neighbors of the cell to the
    # current cell's left to find the next edge
    for x in count(start=2):
        coord = Vector(x=x, y=0)
        left_coord = Vector(x=x-1, y=0)
        left_id = grid[left_coord]

        neighbor_nodes = lookup[left_id]
        missing_edges = (neighbor_nodes & edges) - placed_nodes
        assert len(missing_edges) == 1

        tile_id = list(missing_edges)[0]
        grid[coord] = tile_id
        placed_nodes.add(tile_id)

        # Stop after we place a corner tile
        if tile_id in corners:
            break

    grid_width = x + 1

    # Do all the remainder rows, loooking at the cell above and placing the only
    # neighbor tile that hasn't been placed yet.
    for y in count(start=1):
        for x in range(0, grid_width):
            coord = Vector(x=x, y=y)
            north_coord = Vector(x=x, y=y-1)
            north_id = grid[north_coord]

            neighbor_nodes = lookup[north_id]

            missing_neighbors = list(neighbor_nodes - placed_nodes)
            assert len(missing_neighbors) == 1

            tile_id = list(missing_neighbors)[0]
            grid[coord] = tile_id
            placed_nodes.add(tile_id)

        if len(grid) >= len(lookup):
            break

    grid_height = y + 1

    return grid, Vector(x=grid_width, y=grid_height)


with open("./data.txt", "r") as fp:
    lines = (line.strip() for line in fp)
    groups = groupby(lines, lambda line: line == "")

    raw_tiles = (group for is_blank, group in groups if not is_blank)

    tiles = (load_tile(tile) for tile in raw_tiles)

    tile_lookup = {
        tile.id: tile for tile in tiles
    }

# Find all edges that match with another tile
edges = tiles_to_shared_edges(tile_lookup.values())

neighbors = vertices_to_adjacency_lookup(edges.values())
print(neighbors)

grid, grid_dimensions = adjacency_lookup_to_grid(neighbors)
print(grid)

corner_coords = [Vector(x=x, y=y) for x in [0, grid_dimensions.x-1] for y in [0, grid_dimensions.y-1]]
corner_tile_ids = [grid[coord] for coord in corner_coords]
assert len(corner_tile_ids) == 4
print(product(corner_tile_ids))
