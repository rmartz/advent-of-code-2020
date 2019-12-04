def get_wire_points(steps):
    def north(x, y, offset):
        return (x, y + offset)

    def south(x, y, offset):
        return (x, y - offset)

    def east(x, y, offset):
        return (x + offset, y)

    def west(x, y, offset):
        return (x - offset, y)

    directions = {
        'U': north,
        'D': south,
        'R': east,
        'L': west
    }

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


def parse_step(step):
    return step[0], int(step[1:])


def get_distance_to_point(steps, target):
    for distance, point in enumerate(get_wire_points(steps), 1):
        if point == target:
            return distance


def get_overlap_latency(wires, pos):
    return sum(
        get_distance_to_point(steps, pos) for steps in wires
    )


with open('data.txt', 'r') as fp:
    wires = [[parse_step(step) for step in line.split(',')] for line in fp]

    positions = (get_wire_points(steps) for steps in wires)

    overlaps = common_positions(positions)

    distances = (get_overlap_latency(wires, overlap) for overlap in overlaps)

    print(min(distances))
