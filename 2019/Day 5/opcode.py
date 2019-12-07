CMD_MAX_SIZE=6

MODE_IMMEDIATE='1'
MODE_POSITION='0'

class Intcode(object):
    _intcode = []
    intcode = []
    input = []
    output = []

    def __init__(self, intcode):
        self._intcode = list(map(int, intcode.split(',')))

    def getval(self, pos, mode):
        if mode == MODE_IMMEDIATE:
            return self.intcode[pos]
        if mode == MODE_POSITION:
            pos = int(self.intcode[pos])
            return int(self.intcode[pos])
        raise Exception(f"Unknown mode '{mode}'")

    def setval(self, pos, val):
        self.intcode[pos] = val

    def next_input(self):
        return next(self.input)

    def add_output(self, val):
        self.output.append(val)

    def getop(self, cmd):
        opsmap = {
            '01': AddOp,
            '02': MultiplyOp,
            '03': InputOp,
            '04': OutputOp,
            '99': HaltOp
        }
        code = cmd[-2:]
        return opsmap[code]()

    def step(self, pos):
        cmd = str(self.getval(pos, MODE_IMMEDIATE)).zfill(CMD_MAX_SIZE)
        op = self.getop(cmd)
        return op.execute_op(self, cmd, pos)

    def run_program(self, input):
        self.intcode = self._intcode[:]
        self.input = iter(input)
        self.output = []

        try:
            pos = 0
            while True:
                pos = self.step(pos)
        except StopIteration:
            pass

        return self.output, self.intcode


class BaseOp(object):
    # The number of arguments this operation takes
    size = None

    def get_flags(self, cmd):
        start = CMD_MAX_SIZE - 2 - self.size
        return list(cmd[start:start+self.size])[::-1]

    def execute_op(self, intcode, cmd, pos):
        flags = self.get_flags(cmd)

        vals = [
            intcode.getval(index, mode)
            for index, mode in enumerate(flags, pos + 1)
        ]

        self.process(intcode, vals)

        return self.next_pos(pos)

    def next_pos(self, pos):
        return pos + self.size + 1

    def process(self, intcode, vals):
        raise NotImplementedError()


class WriteOp(BaseOp):
    def get_flags(self, cmd):
        # Write operations always write to the position in their last argument
        # To avoid double-indirection, make this implicitly IMMEDIATE
        flags = super().get_flags(cmd)
        flags[-1] = MODE_IMMEDIATE
        return flags


class AddOp(WriteOp):
    size = 3

    def process(self, intcode, vals):
        valA, valB, dst = vals
        intcode.setval(dst, valA + valB)


class MultiplyOp(WriteOp):
    size = 3

    def process(self, intcode, vals):
        valA, valB, dst = vals
        intcode.setval(dst, valA * valB)


class InputOp(WriteOp):
    size = 1

    def process(self, intcode, vals):
        dst = vals[0]
        intcode.setval(dst, intcode.next_input())

class OutputOp(BaseOp):
    size = 1

    def process(self, intcode, vals):
        val = vals[0]
        intcode.add_output(val)

class HaltOp(BaseOp):
    size = 0

    def process(self, intcode, vals):
        raise StopIteration



def test_multiply():
    machine = Intcode('1002,4,3,4,33')

    # Should halt
    machine.run_program([])

def test_input_output():
    machine = Intcode('3,0,4,0,99')

    # Should halt
    output, _ = machine.run_program([50])
    assert output == [50]


def test_negative():
    machine = Intcode('1101,100,-1,4,0')

    # Should halt
    machine.run_program([])

test_multiply()
test_input_output()
test_negative()

with open('data.txt', 'r') as fp:
    machine = Intcode(fp.read())

    output, _ = machine.run_program([1])
    assert all(lambda v: v == 0 for v in output[:-1])
    print(output[-1])


