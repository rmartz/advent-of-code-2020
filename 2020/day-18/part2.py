from itertools import zip_longest
from functools import reduce
import re


def product(it):
    return reduce(lambda val, acc: val * acc, it, 1)


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
    product_groups = expression.split(' * ')
    summed_values = (sum(int(val) for val in term.split(' + ')) for term in product_groups)
    return product(summed_values)


def process_expression(expression):
    while '(' in expression:
        expression = evaluate_parentheses_level(expression)

    return eval_expression(expression)


assert process_expression('2 * 3 + (4 * 5)') == 46
assert process_expression('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
assert process_expression('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
assert process_expression('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340

with open("./data.txt", "r") as fp:
    values = (process_expression(line) for line in fp)
    print(sum(values))

