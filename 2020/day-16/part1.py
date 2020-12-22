from itertools import groupby


def parse_rules(rules):
    for interval in rules.split(" or "):
        low, high = (int(v) for v in interval.split("-"))
        yield range(low, high + 1)


def parse_field_line(line):
    # Return a tuple of (field, rules), where rules is a list of range() objects
    field, rules = line.split(": ")
    return (field, list(parse_rules(rules)))


def parse_field_input(field_lines):
    field_rule_pairs = map(parse_field_line, field_lines)
    return {field: rules for field, rules in field_rule_pairs}


def parse_ticket_input(ticket):
    # Our ticket is defined in two lines
    # First line we can ignore, the second has our values
    next(ticket)
    return next(ticket).split(",")


def parse_nearby_input(nearby_lines):
    # First line is the heading "nearby tickets:", so we want to skip it
    next(nearby_lines)
    for line in nearby_lines:
        values = line.split(",")
        yield (int(val) for val in values)


def valid_value(fields, val):
    for rules in fields.values():
        if any(val in interval for interval in rules):
            return True
    return False


def find_invalid_fields(fields, tickets):
    for ticket in tickets:
        for value in ticket:
            if not valid_value(fields, value):
                yield value


with open("./data.txt", "r") as fp:
    lines = (line.strip() for line in fp)
    groups = groupby(lines, lambda line: line == "")

    segments = (group for is_blank, group in groups if not is_blank)

    # First segment is fields
    field_lines = next(segments)
    fields = parse_field_input(field_lines)
    print(fields)

    # Second segment is our ticket
    ticket_lines = next(segments)
    our_ticket = parse_ticket_input(ticket_lines)

    # Third segment is nearby tickets
    nearby_lines = next(segments)
    nearby_values = parse_nearby_input(nearby_lines)

    print(sum(find_invalid_fields(fields, nearby_values)))
