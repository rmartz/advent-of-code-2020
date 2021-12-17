import re

parse_re = re.compile(
    r"(?P<min>[0-9]+)-(?P<max>[0-9]+) (?P<term>[a-z]): (?P<password>[a-z]+)"
)


def validate_line(line):
    matches = parse_re.match(line)
    interval = range(
        int(matches.group("min")),
        int(matches.group("max")) + 1,
    )

    total = sum(1 for c in matches.group("password") if c == matches.group("term"))
    return total in interval


with open("./data.txt", "r") as fp:
    data = fp.readlines()

print(sum(1 for line in data if validate_line(line)))
