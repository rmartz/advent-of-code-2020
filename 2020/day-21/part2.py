from collections import defaultdict
from operator import itemgetter


def parse_input_line(line):
    ingredients, allergens = line.strip(")").split(" (contains ")

    return (set(ingredients.split(" ")), set(allergens.split(", ")))


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


def find_valid_allergen_permutations(allergens, allergen_possibilities):
    # Finds permutations of allergens that comply with all allergen_possibilities constraints
    # Sort allergen_possibilities so the most constrained allergens are first
    # But make a mapping to the original lookup to re-arrange after

    sorted_pairs = sorted(allergen_possibilities.items(), key=lambda item: len(item[1]))
    original_key, ordered_allergen_possibilities = zip(*sorted_pairs)

    valid_permutations = find_valid_permutation(
        set(allergens), ordered_allergen_possibilities
    )
    for permutation in valid_permutations:
        reordered_permutation = {
            key: value for key, value in zip(original_key, permutation)
        }
        yield reordered_permutation


def find_possible_allergens(input):
    ingredient_food_count = defaultdict(int)
    allergen_possibilities = {}
    for line in input:
        ingredients, allergens = parse_input_line(line)
        for ingredient in ingredients:
            ingredient_food_count[ingredient] += 1
        for allergen in allergens:
            try:
                # An allergen can only be caused by a single ingredient (...),
                # so it can only be in ingredients common among all foods that it
                # is reported in
                allergen_possibilities[allergen] &= ingredients
            except KeyError:
                # First time we see an allergen, it could be any of the ingredients
                allergen_possibilities[allergen] = set(ingredients)

    return list(
        find_valid_allergen_permutations(
            set.union(*allergen_possibilities.values()), allergen_possibilities
        )
    )


with open("./data.txt", "r") as fp:
    lines = (line.strip() for line in fp)
    allergen_mappings = find_possible_allergens(lines)

    assert len(allergen_mappings) == 1
    allergen_mapping = allergen_mappings[0]

    print(
        ",".join(
            ingredient
            for _, ingredient in sorted(allergen_mapping.items(), key=itemgetter(0))
        )
    )
