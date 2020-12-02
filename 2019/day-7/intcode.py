CMD_MAX_SIZE=6

MODE_IMMEDIATE='1'
MODE_POSITION='0'


class IncompleteExecutionError(Exception):
    pass

class HaltExecutionError(Exception):
    pass

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
        try:
            return next(self.input)
        except StopIteration:
            raise IncompleteExecutionError()

    def add_output(self, val):
        self.output.append(val)

    def getop(self, cmd):
        opsmap = {
            '01': AddOp,
            '02': MultiplyOp,
            '03': InputOp,
            '04': OutputOp,
            '05': JumpIfTrueOp,
            '06': JumpIfFalseOp,
            '07': LessThanOp,
            '08': EqualsOp,
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
        except HaltExecutionError:
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

        return self.process(intcode, vals, pos)

    def process(self, intcode, vals, pos):
        self.perform_side_effect(intcode, vals)

        return pos + self.size + 1

    def perform_side_effect(self, intcode, vals):
        pass


class WriteOp(BaseOp):
    def get_flags(self, cmd):
        # Write operations always write to the position in their last argument
        # To avoid double-indirection, make this implicitly IMMEDIATE
        flags = super().get_flags(cmd)
        flags[-1] = MODE_IMMEDIATE
        return flags


class AddOp(WriteOp):
    size = 3

    def perform_side_effect(self, intcode, vals):
        valA, valB, dst = vals
        intcode.setval(dst, valA + valB)


class MultiplyOp(WriteOp):
    size = 3

    def perform_side_effect(self, intcode, vals):
        valA, valB, dst = vals
        intcode.setval(dst, valA * valB)

class LessThanOp(WriteOp):
    size = 3

    def perform_side_effect(self, intcode, vals):
        valA, valB, dst = vals

        intcode.setval(dst, 1 if valA < valB else 0)

class EqualsOp(WriteOp):
    size = 3

    def perform_side_effect(self, intcode, vals):
        valA, valB, dst = vals

        intcode.setval(dst, 1 if valA == valB else 0)

class InputOp(WriteOp):
    size = 1

    def perform_side_effect(self, intcode, vals):
        dst = vals[0]
        intcode.setval(dst, intcode.next_input())

class OutputOp(BaseOp):
    size = 1

    def perform_side_effect(self, intcode, vals):
        val = vals[0]
        intcode.add_output(val)

class JumpIfTrueOp(BaseOp):
    size = 2

    def process(self, intcode, vals, pos):
        if vals[0] != 0:
            return vals[1]
        return super().process(intcode, vals, pos)

class JumpIfFalseOp(BaseOp):
    size = 2

    def process(self, intcode, vals, pos):
        if vals[0] == 0:
            return vals[1]
        return super().process(intcode, vals, pos)

class HaltOp(BaseOp):
    size = 0

    def perform_side_effect(self, intcode, vals):
        raise HaltExecutionError



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

def test_equal_pos():
    machine = Intcode('3,9,8,9,10,9,4,9,99,-1,8')

    output, _ = machine.run_program([8])
    assert output == [1]

    output, _ = machine.run_program([9])
    assert output == [0]

def test_less_than_pos():
    machine = Intcode('3,9,7,9,10,9,4,9,99,-1,8')

    output, _ = machine.run_program([8])
    assert output == [0]

    output, _ = machine.run_program([7])
    assert output == [1]

def test_equal_immediate():
    machine = Intcode('3,3,1108,-1,8,3,4,3,99')

    output, _ = machine.run_program([8])
    assert output == [1]

    output, _ = machine.run_program([9])
    assert output == [0]

def test_less_than_immediate():
    machine = Intcode('3,3,1107,-1,8,3,4,3,99')

    output, _ = machine.run_program([8])
    assert output == [0]

    output, _ = machine.run_program([7])
    assert output == [1]


test_multiply()
test_input_output()
test_negative()
test_equal_pos()
test_less_than_pos()
test_equal_immediate()
test_less_than_immediate()
