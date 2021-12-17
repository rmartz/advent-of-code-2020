import re

parse_re = re.compile(
    r"(?P<left>[0-9]+)-(?P<right>[0-9]+) (?P<term>[a-z]): (?P<password>[a-z]+)"
)


def term_check(term, password, index):
    try:
        return password[int(index) - 1] == term
    except Exception:
        return False


def validate_line(line):
    matches = parse_re.match(line)

    term = matches.group("term")
    password = matches.group("password")

    left_match = term_check(term, password, matches.group("left"))
    right_match = term_check(term, password, matches.group("right"))

    return left_match != right_match


with open("./data.txt", "r") as fp:
    data = fp.readlines()

print(sum(1 for line in data if validate_line(line)))
