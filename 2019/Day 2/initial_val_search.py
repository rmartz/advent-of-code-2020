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


def test_initial_state(intcode, noun, verb):
    intcode[1] = noun
    intcode[2] = verb

    result = process_ops(intcode)
    return result[0]


def counting_tuples(digits):
    if digits <= 0:
        yield tuple()
        return

    max_sum = 0
    while True:
        for subset in counting_tuples(digits - 1):
            sub_sum = sum(subset)
            if sub_sum > max_sum:
                break
            yield (max_sum - sub_sum,) + subset
        max_sum += 1

def search_for_initial_state(intcode, target_val):
    for noun, verb in counting_tuples(2):
        if test_initial_state(intcode[:], noun, verb) == target_val:
            return noun, verb


with open('data.txt', 'r') as fp:
    intcode = list(map(int, fp.read().split(',')))

    noun, verb = search_for_initial_state(intcode, 19690720)
    print(100 * noun + verb)
