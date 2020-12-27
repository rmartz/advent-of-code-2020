from itertools import groupby
from collections import namedtuple
from operator import itemgetter


State = namedtuple("State", ["decks"])


def load_deck(input):
    # First line for each deck is a label marking it as a deck, we can ignore that
    next(input)

    # Next is a list of cards, one card per line
    return tuple(int(val) for val in input)


def draw_cards(state):
    draws = [deck[0] for deck in state.decks]
    return draws, State(decks=tuple(tuple(deck[1:]) for deck in state.decks))


def award_win(state, pot, winner):
    loser = 1 - winner
    pot = tuple([pot[winner]] + [pot[loser]])
    return State(
        decks=tuple(
            deck + pot if player == winner else deck
            for player, deck in enumerate(state.decks)
        )
    )


def create_sub_state(state, draws):
    return State(decks=tuple(deck[:card] for deck, card in zip(state.decks, draws)))


def play_round(state):
    draws, state = draw_cards(state)

    if all(card <= len(deck) for card, deck in zip(draws, state.decks)):
        sub_state = create_sub_state(state, draws)
        winner, _ = play_game(sub_state)
    else:
        winner, _ = max(enumerate(draws), key=itemgetter(1))

    return award_win(state, draws, winner)


def play_game(state):
    # Returns a tuple of (winner, winning deck)
    history = set()
    while all(state.decks):
        if state in history:
            return 0, state.decks[0]
        history.add(state)
        state = play_round(state)
    # After a player has lost, the winner is the only non-empty deck
    return next(filter(itemgetter(1), enumerate(state.decks)))


def score_deck(deck):
    return sum(pos * card for pos, card in enumerate(deck[::-1], start=1))


with open("./data.txt", "r") as fp:
    lines = (line.strip() for line in fp)
    groups = groupby(lines, lambda line: line == "")

    game = State(
        decks=tuple(load_deck(lines) for is_blank, lines in groups if not is_blank)
    )

    winner, winning_deck = play_game(game)
    print(score_deck(winning_deck))
