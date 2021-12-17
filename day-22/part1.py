from itertools import groupby
from operator import itemgetter


def load_deck(input):
    # First line for each deck is a label marking it as a deck, we can ignore that
    next(input)

    # Next is a list of cards, one card per line
    return [int(val) for val in input]


def play_game(decks):
    while all(decks):
        draws = [deck.pop(0) for deck in decks]
        winner, card = max(enumerate(draws), key=itemgetter(1))
        decks[winner].extend(sorted(draws, reverse=True))
    return decks[winner]


def score_deck(deck):
    return sum(pos * card for pos, card in enumerate(deck[::-1], start=1))


with open("./data.txt", "r") as fp:
    lines = (line.strip() for line in fp)
    groups = groupby(lines, lambda line: line == "")

    decks = [load_deck(lines) for is_blank, lines in groups if not is_blank]

    print(score_deck(play_game(decks)))
