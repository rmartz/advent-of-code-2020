from collections import namedtuple, defaultdict
from itertools import groupby
from functools import reduce
from enum import Enum


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

    def opposite(direction):
        return {
            Direction.North: Direction.South,
            Direction.South: Direction.North,
            Direction.East: Direction.West,
            Direction.West: Direction.East,
        }[direction]


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


def remainder(lst):
    for i, val in enumerate(lst):
        yield val, lst[:i] + lst[i + 1 :]


def count(start=0, step=1):
    i = start
    while True:
        yield i
        i += step


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
        return {
            Direction.North: raw[0],
            Direction.South: raw[-1][::-1],
            Direction.East: "".join(line[-1] for line in raw),
            Direction.West: "".join(line[0] for line in raw[::-1]),
        }

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
        self.edges = {
            Direction.North: str(self.edges[Direction.South][::-1]),
            Direction.South: str(self.edges[Direction.North][::-1]),
            Direction.East: str(self.edges[Direction.East][::-1]),
            Direction.West: str(self.edges[Direction.West][::-1]),
        }

    def flip(self):
        # Because flipping horizontally is equivalent to flipping vertically and
        # rotating 180 degrees, we only need to implement flipping on one axis
        self._flip_content_horizontally()
        self._flip_edges_horizontally()

    def _rotate_content_clockwise(self):
        pass

    def _rotate_edges_clockwise(self):
        self.edges = {
            Direction.North: self.edges[Direction.West],
            Direction.South: self.edges[Direction.East],
            Direction.East: self.edges[Direction.North],
            Direction.West: self.edges[Direction.South],
        }

    def rotate(self):
        self._rotate_content_clockwise()
        self._rotate_edges_clockwise()


def load_tile(lines):
    label = next(lines)
    raw = list(lines)

    return Tile(
        # The label is always formatted as "Tile {id}:"
        id=int(str(label[5:-1])),
        raw=raw,
    )


def tiles_to_shared_edges(tiles):
    edges = defaultdict(list)
    for tile in tiles:
        for edge in tile.edges.values():
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
            neighbor_lookup[node] |= set(neighbors)
    return neighbor_lookup


def align_tile_to_base(base, direction, tile):
    # Assume base is correct, and this tile is to that direction of the base
    # Determine if this tile needs to be flipped, and then rotate until it fits
    canonical_edge = base.edges[direction]
    mirrored_canonical_edges = set([canonical_edge, canonical_edge[::-1]])

    print(mirrored_canonical_edges)
    print(tile.edges)
    assert set(tile.edges.values()) & mirrored_canonical_edges

    # Rotate until our opposite edge fits the base tile's chosen side
    matching_direction = direction.opposite()
    while tile.edges[matching_direction] not in mirrored_canonical_edges:
        tile.rotate()

    if tile.edges[matching_direction] != canonical_edge:
        # The tile is on the right side, but backwards
        # Flip the tile then find it's true rotation
        tile.flip()
        if tile.edges[matching_direction] != canonical_edge:
            tile.rotate()
            tile.rotate()

    print(tile.edges)
    assert tile.edges[matching_direction] == canonical_edge


def pick_corner_east_neighbor(tile_by_id, lookup, corner):
    # A corner has two neighbors that form a 90-degree angle.
    # We want this corner tile to be in the NW corner, and the algorithm operates row
    #  by row west to east, meaning we want to find the neighbor that will be to the
    #  east when the adjacent neighbor is to the south.
    # We do not need to worry about flipping the corner tile - just rotating it until
    # its neighbored edges are East and South, align the neighbor, then return its ID
    all_neighbor_edges = set()
    corner_edges = set(corner.edges.values())
    for neighbor_id in lookup[corner.id]:
        neighbor = tile_by_id[neighbor_id]
        for edge in neighbor.edges.values():
            # Depending on rotation and flipping the edge could be in either direction
            # We'll figure the right orientation later, right now we just want to find
            # if an matching edge exists
            mirrored_set = set([edge, edge[::-1]])

            # Is there an item in mirrored_set that's also in corner_edges?
            if mirrored_set & corner_edges:
                all_neighbor_edges |= mirrored_set
                break

    # Rotate the corner piece until it's aligned with the NW corner
    # That is, it's only neighbors are to the East and South
    while (
        len(
            set([corner.edges[Direction.East], corner.edges[Direction.South]])
            & all_neighbor_edges
        )
        < 2
    ):
        corner.rotate()

    east_edge = corner.edges[Direction.East]
    mirrored_east_edges = set([east_edge, east_edge[::-1]])
    for neighbor_id in lookup[corner.id]:
        neighbor = tile_by_id[neighbor_id]
        if mirrored_east_edges & set(neighbor.edges.values()):
            print(mirrored_east_edges)
            print(neighbor.edges.values())
            print(mirrored_east_edges & set(neighbor.edges.values()))
            return neighbor_id

    raise Exception("No matching neighbor found")


def adjacency_lookup_to_grid(tile_by_id, lookup):
    edges = set(id for id, neighbors in lookup.items() if len(neighbors) <= 3)
    corners = set(id for id in edges if len(lookup[id]) == 2)

    # Find a corner arbitrarily and set it as (0, 0)
    corner_id = list(corners)[0]
    corner = tile_by_id[corner_id]

    # Because the starting corner has two unplaced edge neighbors, the algorithm won't
    # work on the first edge we place. We need to orient the corner we chose to be the
    #  NW corner, find the file directly to its east, then orient the tile to our chosen
    #  corner manually.
    east_neighbor_id = pick_corner_east_neighbor(tile_by_id, lookup, corner)

    print(corner.edges)
    print(tile_by_id[east_neighbor_id].edges)

    align_tile_to_base(corner, Direction.East, tile_by_id[east_neighbor_id])

    grid = {Vector(x=0, y=0): corner_id, Vector(x=1, y=0): east_neighbor_id}

    placed_ids = set(grid.values())

    # Place the first line left to right, using the edge neighbors of the cell to the
    # current cell's left to find the next edge
    for x in count(start=2):
        coord = Vector(x=x, y=0)
        west_coord = Vector(x=x - 1, y=0)
        west_id = grid[west_coord]

        neighbor_ids = lookup[west_id]
        missing_edges = (neighbor_ids & edges) - placed_ids
        assert len(missing_edges) == 1

        tile_id = list(missing_edges)[0]

        print(coord)
        print(tile_id)
        print(neighbor_ids)
        print(tile_by_id[west_id].edges)
        print(tile_by_id[tile_id].edges)

        # Our new tile is on the east edge of our western neighbor
        align_tile_to_base(tile_by_id[west_id], Direction.East, tile_by_id[tile_id])

        grid[coord] = tile_id
        placed_ids.add(tile_id)

        # Stop after we place a corner tile
        if tile_id in corners:
            break

    grid_width = x + 1

    # Do all the remainder rows, loooking at the cell above and placing the only
    # neighbor tile that hasn't been placed yet.
    for y in count(start=1):
        for x in range(0, grid_width):
            coord = Vector(x=x, y=y)
            north_coord = Vector(x=x, y=y - 1)
            north_id = grid[north_coord]

            neighbor_ids = lookup[north_id]

            missing_neighbors = list(neighbor_ids - placed_ids)
            assert len(missing_neighbors) == 1

            tile_id = list(missing_neighbors)[0]

            print("=======")
            print(f"Determining tile for coordinates {coord}")
            print(f"Only unplaced neighbor tile for {north_id} is {tile_id}")
            print(f"(All possible neighbors was {neighbor_ids})")
            if x > 0:
                west_coord = Vector(x=x-1, y=y)
                west_id = grid[west_coord]
                print(f"(All possible neighbors to our west was {lookup[west_id]})")
                print(f"East edge of tile to the west: {tile_by_id[west_id].edges[Direction.East]}")
            print(f"South edge of tile to the north: {tile_by_id[north_id].edges[Direction.South]}")
            print(f"Edges of tile being placed: {tile_by_id[tile_id].edges}")

            # Our new tile is on the south edge of our northern neighbor
            align_tile_to_base(
                tile_by_id[north_id], Direction.South, tile_by_id[tile_id]
            )

            grid[coord] = tile_id
            placed_ids.add(tile_id)

        if len(grid) >= len(lookup):
            break

    grid_height = y + 1

    return grid, Vector(x=grid_width, y=grid_height)


with open("./data.txt", "r") as fp:
    lines = (line.strip() for line in fp)
    groups = groupby(lines, lambda line: line == "")

    raw_tiles = (group for is_blank, group in groups if not is_blank)

    tiles = (load_tile(tile) for tile in raw_tiles)

    tile_lookup = {tile.id: tile for tile in tiles}

# Find all edges that match with another tile
edges = tiles_to_shared_edges(tile_lookup.values())
print(edges)

neighbors = vertices_to_adjacency_lookup(edges.values())
print(neighbors)

grid, grid_dimensions = adjacency_lookup_to_grid(tile_lookup, neighbors)
print(grid_dimensions)


corner_coords = [
    Vector(x=x, y=y)
    for x in [0, grid_dimensions.x - 1]
    for y in [0, grid_dimensions.y - 1]
]
corner_tile_ids = [grid[coord] for coord in corner_coords]
assert len(corner_tile_ids) == 4
print(product(corner_tile_ids))
