from itertools import groupby, permutations
from functools import reduce


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


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
    return (int(v) for v in next(ticket).split(","))


def parse_nearby_input(nearby_lines):
    # First line is the heading "nearby tickets:", so we want to skip it
    next(nearby_lines)
    for line in nearby_lines:
        values = line.split(",")
        yield list(int(val) for val in values)


def matching_rule(rule, val):
    return any(val in interval for interval in rule)


def valid_value(fields, val):
    for rule in fields.values():
        if matching_rule(rule, val):
            return True
    return False


def valid_ticket(fields, ticket):
    # A ticket is valid if all of its fields are valid and follow at least one rule
    return all(valid_value(fields, value) for value in ticket)


def filter_field_rules(fields, fields_options, ticket):
    for rules, value in zip(fields_options, ticket):
        yield set(rule for rule in rules if matching_rule(fields[rule], value))


def find_valid_permutation(values, values_options):
    if not values_options:
        yield []

    for options in values_options:
        if not (values & options):
            # We made a selection that made some later item unsatisfiable
            # All subtrees are invalid, so quit now
            raise Exception("Invalid tree")

    valid_options = values & values_options[0]
    remaining_options = values_options[1:]
    for option in valid_options:
        remaining_values = values - set([option])
        try:
            for suffix in find_valid_permutation(remaining_values, remaining_options):
                yield [option] + suffix
        except Exception:
            pass


def find_valid_field_permutations(fields, fields_options):
    # Finds permutations of fields that comply with all fields_options constraints
    # Sort fields_options so the most constrained fields are first
    # But record the original order to re-arrange after

    sorted_pairs = sorted(enumerate(fields_options), key=lambda pair: len(pair[1]))
    original_order, ordered_fields_options = zip(*sorted_pairs)

    # Reverse the lookup so we know which position to grab for each position in the output
    reverse_pos_order = [
        new_pos
        for new_pos, _ in sorted(enumerate(original_order), key=lambda pair: pair[1])
    ]

    valid_permutations = find_valid_permutation(
        set(fields.keys()), ordered_fields_options
    )
    for permutation in valid_permutations:
        reordered_permutation = [permutation[pos] for pos in reverse_pos_order]
        yield reordered_permutation


def find_field_position_options(fields, valid_tickets):
    # Returns a list containing the set of fields that could apply to that corresponding position
    first = next(valid_tickets)

    fields_options = filter_field_rules(
        fields, [set(fields.keys())] * len(first), first
    )

    for ticket in valid_tickets:
        fields_options = filter_field_rules(fields, fields_options, ticket)

    return fields_options


with open("./data.txt", "r") as fp:
    lines = (line.strip() for line in fp)
    groups = groupby(lines, lambda line: line == "")

    segments = (group for is_blank, group in groups if not is_blank)

    # First segment is fields
    field_lines = next(segments)
    fields = parse_field_input(field_lines)

    # Second segment is our ticket
    ticket_lines = next(segments)
    our_ticket = parse_ticket_input(ticket_lines)

    # Third segment is nearby tickets
    nearby_lines = next(segments)
    nearby_tickets = parse_nearby_input(nearby_lines)

    valid_nearby_tickets = (
        ticket for ticket in nearby_tickets if valid_ticket(fields, ticket)
    )

    fields_options = list(find_field_position_options(fields, valid_nearby_tickets))

    valid_permutations = list(find_valid_field_permutations(fields, fields_options))

    for permutation in valid_permutations:
        aligned_fields = zip(our_ticket, permutation)
        matching_fields = (
            val for val, field in aligned_fields if field.startswith("departure")
        )
        print(product(matching_fields))
