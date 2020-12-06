from itertools import permutations
from intcode import Intcode


def test_phase_sequence(machine, sequence):
    signal = 0
    for setting in sequence:
        output, _ = machine.run_program([setting, signal])
        signal = output[0]
    return signal


def test_max_thruster_1():
    machine = Intcode("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")

    val = test_phase_sequence(machine, [4, 3, 2, 1, 0])
    assert val == 43210


def test_max_thruster_2():
    machine = Intcode(
        "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
    )

    val = test_phase_sequence(machine, [0, 1, 2, 3, 4])
    assert val == 54321


def test_max_thruster_3():
    machine = Intcode(
        "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
    )

    val = test_phase_sequence(machine, [1, 0, 4, 3, 2])
    assert val == 65210


test_max_thruster_1()
test_max_thruster_2()
test_max_thruster_3()


with open("data.txt", "r") as fp:
    machine = Intcode(fp.read())

    print(
        max(
            test_phase_sequence(machine, combination)
            for combination in permutations(range(5))
        )
    )
