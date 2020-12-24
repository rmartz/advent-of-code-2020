from functools import lru_cache
from itertools import groupby
import re


rules = {}


@lru_cache
def generate_regex(id):
    global rules
    rule = rules[id]
    if type(rule) == str:
        return rule

    # Otherwise the rule is a list of possible rules that we want to evaluate and combine
    parts = ["".join(generate_regex(sub_id) for sub_id in branch) for branch in rule]

    return f"({'|'.join(parts)})"


def load_rule(line):
    id, rule = line.split(": ")
    id = int(id)
    if '"' in rule:
        return (id, rule[1])

    branches = rule.split(" | ")
    sub_ids = [[int(id) for id in branch.split(" ")] for branch in branches]
    return (id, sub_ids)


def load_rules(lines):
    rules = (load_rule(line) for line in lines)
    return {id: rule for id, rule in rules}


def check_input(regex, line):
    return regex.match(line)


def find_matching_lines(rule_id, lines):
    rule_regex = re.compile(f"^{generate_regex(rule_id)}$")
    for line in lines:
        if rule_regex.match(line):
            yield line


with open("./data.txt", "r") as fp:
    lines = (line.strip() for line in fp)
    groups = groupby(lines, lambda line: line == "")

    segments = (group for is_blank, group in groups if not is_blank)

    # First segment is rules
    rule_lines = next(segments)
    rules = load_rules(rule_lines)

    # Second segment is strings to match
    input_lines = next(segments)
    matching_lines = find_matching_lines(0, input_lines)
    print(sum(1 for line in matching_lines))
