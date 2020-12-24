from itertools import zip_longest
import re
import operator

PAREN_REGEX = re.compile('\(([^()]*)\)')


def evaluate_parentheses_level(expression):
    def sub_func(match):
        expression = match.group(1)
        return str(eval_expression(expression))
    return PAREN_REGEX.sub(sub_func, expression)


def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)


def eval_expression(expression):
    operations = {
        '+': operator.add,
        '*': operator.mul
    }

    terms = expression.split(' ')
    result = int(terms.pop(0))
    for operation, val in grouper(2, terms):
        func = operations[operation]
        result = func(result, int(val))
    return result


def process_expression(expression):
    while '(' in expression:
        expression = evaluate_parentheses_level(expression)

    return eval_expression(expression)


assert eval_expression('1 + 2 * 3 + 4 * 5 + 6') == 71
assert process_expression('2 * 3 + (4 * 5)') == 26
assert process_expression('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert process_expression('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert process_expression('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

with open("./data.txt", "r") as fp:
    values = (process_expression(line) for line in fp)
    print(sum(values))

