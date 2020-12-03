from collections import namedtuple


Grid = namedtuple("grid", ["cells", "height", "width"])
TREE = '#'

Vector = namedtuple("slope", ["x", "y"])


def addVectors(a, b):
    return Vector(x=a.x + b.x, y=a.y + b.y)


def lookupCell(grid, pos):
    # Maps repeat horizontally
    j = pos.x % grid.width
    # ...but not vertically
    i = pos.y
    return (i, j) in grid.cells


def createGrid(input):
    cells = set()
    for i, row in enumerate(input):
        for j, cell in enumerate(row):
            if cell == TREE:
                cells.add((i, j))

    return Grid(
        cells=cells,
        height=i,
        width=j
    )


def traverseGrid(grid: Grid, slope: Vector):
    pos = Vector(x=0, y=0)
    while pos.y <= grid.height:
        yield lookupCell(grid, pos)
        pos = addVectors(pos, slope)


with open('./data.txt', 'r') as fp:
    grid = createGrid(fp)

slope = Vector(x=3, y=1)
path = traverseGrid(grid, slope)
print(sum(1 for tree in path if tree))
