from collections import namedtuple

Vector = namedtuple("Vector", ["x", "y"])


def add_vectors(a: Vector, b: Vector) -> Vector:
    return Vector(x=a.x + b.x, y=a.y + b.y)


def count(start=0, step=1):
    i = start
    while True:
        yield i
        i += step


ADJACENCIES = [
    Vector(x=x, y=y) for x in [-1, 0, 1] for y in [-1, 0, 1] if x != 0 or y != 0
]

max_x = None
max_y = None


def find_nearest_seat(grid, seat, direction):
    global max_x
    global max_y

    target = seat

    for step in count(start=1):
        target = add_vectors(target, direction)
        if target.x < 0 or target.y < 0 or target.x > max_x or target.y > max_y:
            raise Exception("No nearest seat found")
        if target in grid:
            return target


def get_visible_seats(grid, seat):
    for neighbor in ADJACENCIES:
        try:
            yield find_nearest_seat(grid, seat, neighbor)
        except Exception:
            pass


def get_occupied_neighbor_count(grid, seat):
    return sum(1 for neighbor in get_visible_seats(grid, seat) if grid.get(neighbor))


def get_changes(grid):
    for seat, isOccupied in grid.items():
        occupied_neighbors = get_occupied_neighbor_count(grid, seat)
        if isOccupied:
            if occupied_neighbors >= 5:
                yield seat
        else:
            if occupied_neighbors == 0:
                yield seat


def apply_changes(grid, changes):
    for seat in changes:
        # Use XOR assignment to invert the seat's occupied value
        grid[seat] ^= True


def load_grid(lines):
    global max_x
    global max_y

    grid = {}
    max_x = None
    max_y = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            if c != ".":
                seat = Vector(x=x, y=y)
                grid[seat] = c == "#"
                if max_x is None or max_x < x:
                    max_x = x
                if max_y is None or max_y < y:
                    max_y = y
    return grid


def blank_grid(width, height):
    def blank_row():
        return ["."] * width

    for x in range(height):
        yield list(blank_row())


def print_grid(grid):
    cells = list(blank_grid(max_x + 1, max_y + 1))
    for seat, isOccupied in grid.items():
        cells[seat.y][seat.x] = "#" if isOccupied else "L"

    print("")
    for line in cells:
        print("".join(line))


def test1():
    lines = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
""".split(
        "\n"
    )
    grid = load_grid(lines)
    print_grid(grid)
    visible_occupied_seats = get_occupied_neighbor_count(grid, Vector(x=3, y=4))
    print(visible_occupied_seats)
    assert visible_occupied_seats == 8


def test2():
    lines = """.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
""".split(
        "\n"
    )
    grid = load_grid(lines)
    print_grid(grid)
    visible_occupied_seats = get_occupied_neighbor_count(grid, Vector(x=3, y=3))
    print(visible_occupied_seats)
    assert visible_occupied_seats == 0


# test1()
# test2()

with open("./data.txt", "r") as fp:
    grid = load_grid(fp)

while True:
    changes = list(get_changes(grid))
    if not changes:
        print(sum(1 for isOccupied in grid.values() if isOccupied))
        break
    apply_changes(grid, changes)
