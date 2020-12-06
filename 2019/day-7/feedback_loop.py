from itertools import permutations, cycle
from intcode import Intcode, IncompleteExecutionError


def calculate_feedback_sequence(machine, sequence):
    input = []
    for setting in cycle(sequence):
        if setting == sequence[0]:
            # Prepend 0 for initial machine to start process
            input = [0] + input
        try:
            result, _ = machine.run_program([setting, *input])
        except IncompleteExecutionError:
            pass
        else:
            if setting == sequence[-1]:
                return result[-1]

        input = machine.output


def test_feedback_sequence_1():
    machine = Intcode(
        "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
    )

    val = calculate_feedback_sequence(machine, [9, 8, 7, 6, 5])
    assert val == 139629729


def test_feedback_sequence_2():
    machine = Intcode(
        "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
    )

    val = calculate_feedback_sequence(machine, [9, 7, 8, 5, 6])
    assert val == 18216


test_feedback_sequence_1()
test_feedback_sequence_2()


with open("data.txt", "r") as fp:
    machine = Intcode(fp.read())

    print(
        max(
            calculate_feedback_sequence(machine, combination)
            for combination in permutations([9, 8, 7, 6, 5])
        )
    )
