from intcode import Intcode

with open('data.txt', 'r') as fp:
    machine = Intcode(fp.read())

    output, _ = machine.run_program([1])
    assert len(output) == 1
    print(output[0])


