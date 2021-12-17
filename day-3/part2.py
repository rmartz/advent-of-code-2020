from collections import namedtuple
from functools import reduce


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


Grid = namedtuple("grid", ["cells", "height", "width"])
TREE = "#"

Vector = namedtuple("slope", ["x", "y"])


def addVectors(a: Vector, b: Vector) -> Vector:
    return Vector(x=a.x + b.x, y=a.y + b.y)


def lookupCell(grid: Grid, pos: Vector) -> bool:
    # Maps repeat horizontally
    j = pos.x % grid.width
    # ...but not vertically
    i = pos.y
    return (i, j) in grid.cells


def createGrid(input) -> Grid:
    cells = set()
    for i, row in enumerate(input):
        for j, cell in enumerate(row):
            if cell == TREE:
                cells.add((i, j))

    return Grid(cells=cells, height=i, width=j)


def traverseGrid(grid: Grid, slope: Vector) -> iter:
    pos = Vector(x=0, y=0)
    while pos.y <= grid.height:
        yield lookupCell(grid, pos)
        pos = addVectors(pos, slope)


def countTrees(grid: Grid, slopes: list) -> iter:
    for slope in slopes:
        path = traverseGrid(grid, slope)
        yield sum(1 for tree in path if tree)


with open("./data.txt", "r") as fp:
    grid = createGrid(fp)

slopes = [
    Vector(x=1, y=1),
    Vector(x=3, y=1),
    Vector(x=5, y=1),
    Vector(x=7, y=1),
    Vector(x=1, y=2),
]
treeCounts = countTrees(grid, slopes)

print(product(treeCounts))
