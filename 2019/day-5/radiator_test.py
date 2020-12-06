from intcode import Intcode

with open("data.txt", "r") as fp:
    machine = Intcode(fp.read())

    output, _ = machine.run_program([5])
    assert all(lambda v: v == 0 for v in output[:-1])
    print(output[-1])
