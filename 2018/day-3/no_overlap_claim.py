import re
from collections import defaultdict

cells = {}
candidates = {}

claim_re = re.compile("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")


def parse_claim(claim):
    matches = claim_re.match(claim)
    return [int(v) for v in matches.groups()]


def get_coverage(left, top, width, height):
    for x in range(left, left + width):
        for y in range(top, top + height):
            yield (x, y)


with open("data.txt", "r") as fp:
    for claim in fp:
        id, left, top, width, height = parse_claim(claim)
        candidates[id] = True
        for cell in get_coverage(left, top, width, height):
            if cell in cells:
                candidates[id] = False
                candidates[cells[cell]] = False
            else:
                cells[cell] = id

print(",".join(str(k) for k, v in candidates.items() if v))
