from collections import namedtuple
from itertools import islice

Vector3D = namedtuple("Vector3D", ["x", "y", "z"])


def add_vectors(a: Vector3D, b: Vector3D) -> Vector3D:
    return Vector3D(x=a.x + b.x, y=a.y + b.y, z=a.z + b.z)


ADJACENCIES = [
    Vector3D(x=x, y=y, z=z)
    for x in [-1, 0, 1]
    for y in [-1, 0, 1]
    for z in [-1, 0, 1]
    if x != 0 or y != 0 or z != 0
]


def get_neighbor_cells(grid, cell):
    for neighbor in ADJACENCIES:
        yield add_vectors(cell, neighbor)


def get_active_neighbor_count(grid, cell):
    return sum(1 for neighbor in get_neighbor_cells(grid, cell) if neighbor in grid)


def get_active_cells(grid):
    return grid


def get_accessible_inactive_cells(grid):
    def accessible_cells():
        for cell in grid:
            yield from get_neighbor_cells(grid, cell)

    return set(accessible_cells()) - grid


def get_changes(grid):
    for cell in get_active_cells(grid):
        active_neighbors = get_active_neighbor_count(grid, cell)
        if active_neighbors not in [2, 3]:
            yield cell

    for cell in get_accessible_inactive_cells(grid):
        active_neighbors = get_active_neighbor_count(grid, cell)
        if active_neighbors == 3:
            yield cell


def apply_changes(grid, changes):
    # Use symmetric difference assignment to invert the cells' status
    return grid ^ set(changes)


def step_simulation(grid):
    changes = get_changes(grid)
    return apply_changes(grid, changes)


def run_simulation(grid):
    while True:
        yield grid
        grid = step_simulation(grid)


def load_cells_from_input(lines):
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                yield Vector3D(x=x, y=y, z=0)


def load_grid(lines):
    return set(load_cells_from_input(lines))


def find_range(vals):
    seq = iter(vals)
    low = high = next(seq)
    for val in seq:
        low = min(low, val)
        high = max(high, val)
    return range(low, high + 1)


def print_grid(grid):
    z_range = find_range(v.z for v in grid)
    x_range = find_range(v.x for v in grid)
    y_range = find_range(v.y for v in grid)

    for z in z_range:
        print(f"z={z}")
        for y in y_range:
            print(
                "".join(
                    "#" if Vector3D(x=x, y=y, z=z) in grid else "." for x in x_range
                )
            )

        print("")


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    v = next(islice(iterable, n, None), default)
    return v


with open("./data.txt", "r") as fp:
    grid = load_grid(fp)

result = nth(run_simulation(grid), 6)
print(len(get_active_cells(result)))
