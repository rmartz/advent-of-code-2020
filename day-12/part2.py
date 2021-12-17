from enum import Enum
from collections import namedtuple
from functools import reduce

Ship = namedtuple("Ship", ["pos", "waypoint"])
Vector = namedtuple("Vector", ["x", "y"])
Step = namedtuple("Step", ["action", "value"])


class Action(Enum):
    North = "N"
    South = "S"
    East = "E"
    West = "W"
    Left = "L"
    Right = "R"
    Forwards = "F"


CARDINALS = {
    Action.North: Vector(0, 1),
    Action.South: Vector(0, -1),
    Action.East: Vector(1, 0),
    Action.West: Vector(-1, 0),
}
ANGLES = {
    angle: CARDINALS[direction]
    for angle, direction in [
        (0, Action.North),
        (90, Action.East),
        (180, Action.South),
        (270, Action.West),
    ]
}


def add_vectors(a: Vector, b: Vector) -> Vector:
    return Vector(x=a.x + b.x, y=a.y + b.y)


def scale_vector(a: Vector, scale) -> Vector:
    return Vector(x=a.x * scale, y=a.y * scale)


def rotate_clockwise(a: Vector, rotation):
    rotations = {
        0: lambda a: a,
        90: lambda a: Vector(x=a.y, y=-a.x),
        180: lambda a: Vector(x=-a.x, y=-a.y),
        270: lambda a: Vector(x=-a.y, y=a.x),
    }
    return rotations[rotation](a)


def rotate_quarter_counterclockwise(a: Vector):
    return Vector(x=-a.y, y=a.x)


def move_ship(ship, offset):
    return Ship(
        pos=add_vectors(ship.pos, offset),
        waypoint=ship.waypoint,
    )


def move_waypoint(ship, offset):
    return Ship(
        pos=ship.pos,
        waypoint=add_vectors(ship.waypoint, offset),
    )


def rotate_waypoint(ship, rotation):
    rotation = (rotation + 360) % 360

    return Ship(pos=ship.pos, waypoint=rotate_clockwise(ship.waypoint, rotation))


def process_step(ship, step):
    if step.action == Action.Right:
        return rotate_waypoint(ship, step.value)
    elif step.action == Action.Left:
        return rotate_waypoint(ship, -step.value)

    if step.action == Action.Forwards:
        offset = scale_vector(ship.waypoint, step.value)
        return move_ship(ship, offset)
    else:
        offset = scale_vector(CARDINALS[step.action], step.value)
        return move_waypoint(ship, offset)


def read_step(line):
    return Step(action=Action(line[0]), value=int(line[1:]))


def manhattan_distance(pos):
    return sum(abs(v) for v in [pos.x, pos.y])


with open("./data.txt", "r") as fp:
    steps = (read_step(step) for step in fp)

    ship = reduce(
        process_step, steps, Ship(pos=Vector(x=0, y=0), waypoint=Vector(x=10, y=1))
    )

    print(manhattan_distance(ship.pos))
