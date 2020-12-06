def get_wire_points(steps):
    def north(x, y, offset):
        return (x, y + offset)

    def south(x, y, offset):
        return (x, y - offset)

    def east(x, y, offset):
        return (x + offset, y)

    def west(x, y, offset):
        return (x - offset, y)

    directions = {"U": north, "D": south, "R": east, "L": west}

    x, y = (0, 0)

    for dir, length in steps:
        func = directions[dir]
        for offset in range(length):
            yield func(x, y, offset + 1)
        x, y = func(x, y, length)


def common_positions(wires):
    sets = (set(positions) for positions in wires)
    base = next(sets)
    return base.intersection(*sets)


def manhattan_distance(src, dst):
    return abs(src[0] - dst[0]) + abs(src[1] - dst[1])


def parse_step(step):
    return step[0], int(step[1:])


with open("data.txt", "r") as fp:
    wires = (map(parse_step, line.split(",")) for line in fp)

    positions = (get_wire_points(steps) for steps in wires)

    overlaps = common_positions(positions)

    origin = (0, 0)
    distances = (manhattan_distance(origin, pos) for pos in overlaps)

    print(min(distances))
