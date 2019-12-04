def add_ops(intcode, pos):
    posA, posB, dst = intcode[pos+1:pos+4]
    intcode[dst] = intcode[posA] + intcode[posB]
    return intcode

def multiply_ops(intcode, pos):
    posA, posB, dst = intcode[pos+1:pos+4]
    intcode[dst] = intcode[posA] * intcode[posB]
    return intcode

def process_ops(intcode):
    ops = {
        1: add_ops,
        2: multiply_ops
    }

    pos = 0
    while True:
        cmd = intcode[pos]
        if cmd == 99:
            return intcode
        ops[cmd](intcode, pos)

        pos += 4



with open('data.txt', 'r') as fp:
    intcode = list(map(int, fp.read().split(',')))

    intcode[1] = 12
    intcode[2] = 2

    result = process_ops(intcode)
    print(result[0])
