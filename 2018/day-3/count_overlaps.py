import re
from collections import defaultdict

cells = defaultdict(int)

claim_re = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
def parse_claim(claim):
    matches = claim_re.match(claim)
    return [int(v) for v in matches.groups()]

def get_coverage(claim):
    _, left, top, width, height = parse_claim(claim)
    for x in range(left, left + width):
        for y in range(top, top + height):
            yield (x, y)

with open('data.txt', 'r') as fp:
    for claim in fp:
        for cell in get_coverage(claim):
            cells[cell] += 1

print(sum(1 if val >= 2 else 0 for val in cells.values()))