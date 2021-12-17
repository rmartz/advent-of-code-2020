from itertools import islice
from collections import namedtuple

State = namedtuple("State", ["history", "move", "round"])


def next_val(state):
    try:
        return state.round - state.history[state.move]
    except KeyError:
        return 0


def make_move(prev, move):
    history = prev.history.copy()
    history[prev.move] = prev.round
    return State(history=history, move=move, round=prev.round + 1)


def next_state(state):
    val = next_val(state)
    return make_move(state, val)


def memory_game(seed):
    starting_moves = iter(seed)
    state = State(history={}, move=next(starting_moves), round=0)
    for move in starting_moves:
        yield state.move
        state = make_move(state, move)

    while True:
        yield state.move
        state = next_state(state)


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    v = next(islice(iterable, n - 1, None), default)
    return v


assert list(islice(memory_game([0, 3, 6]), 10)) == [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]
assert nth(memory_game([0, 3, 6]), 4) == 0
assert nth(memory_game([1, 3, 2]), 2020) == 1
assert nth(memory_game([2, 1, 3]), 2020) == 10
assert nth(memory_game([1, 2, 3]), 2020) == 27
assert nth(memory_game([2, 3, 1]), 2020) == 78
assert nth(memory_game([3, 2, 1]), 2020) == 438
assert (
    nth(
        memory_game(
            [
                3,
                1,
                2,
            ]
        ),
        2020,
    )
    == 1836
)


with open("./data.txt", "r") as fp:
    seed = (int(v) for v in fp.read().split(","))
    game = memory_game(seed)
    print(nth(game, 2020))
