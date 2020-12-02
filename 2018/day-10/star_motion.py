from Queue import Queue
from collections import deque
from itertools import islice
import re

line_regex = re.compile('position=< *(-?[0-9]+),  *(-?[0-9]+ *)> velocity=< *(-?[0-9]+), *(-?[0-9]+) *>')
def parse_line(line):
    try:
        regex = map(int, line_regex.match(line).groups())
    except AttributeError:
        raise Exception("Failed to parse line {}".format(line))
    return [regex[:2], regex[2:]]

def calculate_minmax(vals):
    i = iter(vals)

    vmin = vmax = next(i)

    for val in i:
        if val > vmax:
            vmax = val
        if val < vmin:
            vmin = val
    return vmin, vmax

def calculate_bounds(positions):
    xpositions = (v[0] for v in positions)
    ypositions = (v[1] for v in positions)

    return (
        calculate_minmax(xpositions),
        calculate_minmax(ypositions)
    )

def filter_bounding_box(lines, bounding_box):
    def within(val, bounds):
        min, max = bounds
        return val >= min and val <= max
    def in_bounds(line):
        pos, v = line
        x, y = pos
        return within(x, xbounds) and within(y, ybounds)

    xbounds, ybounds = bounding_box
    return filter(in_bounds, lines)

def calculate_positions(lines):
    bounding_box = calculate_bounds([v[0] for v in lines])
    last_n = []
    for i in xrange(1000000):
        print i
        lines = filter_bounding_box(lines, bounding_box)
        if not lines:
            break

        positions = [v[0][:] for v in lines]
        bounding_box = calculate_bounds(positions)

        yield positions

        advance_tick(lines)

def swallow_keyboard_interrupt(i):
    try:
        for pos in i:
            yield pos
    except KeyboardInterrupt:
        return

def draw_starmap(positions, xbounds, ybounds):
    row_width = xbounds[1] - xbounds[0] + 1
    num_cols = ybounds[1] - ybounds[0] + 1

    x_offset = xbounds[0]
    y_offset = ybounds[0]
    normalized_positions = ((x - x_offset, y - y_offset) for x, y in positions)

    pos_map = set()
    for pos in normalized_positions:
        xpos, ypos = pos
        try:
            assert xpos >= 0
            assert xpos < row_width
            assert ypos >= 0
            assert ypos < num_cols
        except AssertionError:
            continue

        pos_map.add(pos)

    print ''
    print ''
    for y in xrange(num_cols):
        row = ['#' if (x, y) in pos_map else ' ' for x in xrange(row_width)]
        print ''.join(row)

def advance_tick(lines):
    for p, v in lines:
        p[0] += v[0]
        p[1] += v[1]


with open('data.txt', 'r') as fp:
    lines = map(parse_line, fp)

    positions = calculate_positions(lines)
    positions_cutoff = swallow_keyboard_interrupt(positions)

    queue = deque(positions_cutoff, 100)

    while True:
        positions = queue.pop()
        xbounds, ybounds = calculate_bounds(positions)
        draw_starmap(positions, xbounds, ybounds)
