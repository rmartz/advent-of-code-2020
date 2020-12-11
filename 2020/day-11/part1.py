from collections import namedtuple

Vector = namedtuple("Vector", ["x", "y"])


def add_vectors(a: Vector, b: Vector) -> Vector:
    return Vector(x=a.x + b.x, y=a.y + b.y)


def scale_vector(a: Vector, scale) -> Vector:
    return Vector(x=a.x * scale, y=a.y * scale)


ADJACENCIES = [
    Vector(x=x, y=y) for x in [-1, 0, 1] for y in [-1, 0, 1] if x != 0 or y != 0
]


def get_neighbor_seats(grid, seat):
    for neighbor in ADJACENCIES:
        yield add_vectors(seat, neighbor)


def get_occupied_neighbor_count(grid, seat):
    return sum(1 for neighbor in get_neighbor_seats(grid, seat) if grid.get(neighbor))


def get_changes(grid):
    for seat, isOccupied in grid.items():
        occupied_neighbors = get_occupied_neighbor_count(grid, seat)
        if isOccupied:
            if occupied_neighbors >= 4:
                yield seat
        else:
            if occupied_neighbors == 0:
                yield seat


def apply_changes(grid, changes):
    for seat in changes:
        # Use XOR assignment to invert the seat's occupied value
        grid[seat] ^= True


def load_seats_from_input(lines):
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "L":
                yield Vector(x=x, y=y)


def load_grid(lines):
    grid = {}
    seats = load_seats_from_input(lines)
    for seat in seats:
        grid[seat] = False
    return grid


with open("./data.txt", "r") as fp:
    grid = load_grid(fp)

while True:
    changes = list(get_changes(grid))
    if not changes:
        print(sum(1 for isOccupied in grid.values() if isOccupied))
        break
    apply_changes(grid, changes)
