from collections import defaultdict


def parse_input_line(line):
    ingredients, allergens = line.strip(')').split(' (contains ')

    return (
        set(ingredients.split(' ')),
        set(allergens.split(', '))
    )


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

    # An ingredient _could_ be allergic if it hasn't been excluded from all allergens
    # Even if an allergen has many potential ingredients, they all could be allergens
    allergic_ingredients = set.union(*allergen_possibilities.values())

    # Sum all of the foods that each known non-allergen ingredient has been in
    return sum(count for ingredient, count in ingredient_food_count.items()
               if ingredient not in allergic_ingredients)


with open("./data.txt", "r") as fp:
    lines = (line.strip() for line in fp)
    mapping = find_possible_allergens(lines)
    print(mapping)
