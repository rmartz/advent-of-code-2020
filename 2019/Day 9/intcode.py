CMD_MAX_SIZE = 6

MODE_IMMEDIATE = '1'
MODE_RELATIVE = '2'
MODE_POSITION = '0'


class IncompleteExecutionError(Exception):
    pass


class HaltExecutionError(Exception):
    pass


class Intcode(object):
    _intcode = []
    intcode = []
    input = []
    output = []
    relative_base = 0

    def __init__(self, intcode):
        self._intcode = list(map(int, intcode.split(',')))

    def get_target_pos(self, pos, mode):
        if mode == MODE_IMMEDIATE:
            return pos
        if mode == MODE_POSITION:
            return self.getval(pos, MODE_IMMEDIATE)
        if mode == MODE_RELATIVE:
            pos = self.get_target_pos(pos, MODE_POSITION)
            return pos + self.relative_base
        raise Exception(f"Unknown mode '{mode}'")

    def getval(self, pos, mode):
        pos = self.get_target_pos(pos, mode)
        try:
            return self.intcode[pos]
        except IndexError:
            if pos >= 0:
                return 0
            raise

    def setval(self, pos, mode, val):
        assert mode != MODE_IMMEDIATE
        pos = self.get_target_pos(pos, mode)
        try:
            self.intcode[pos] = val
        except IndexError:
            growth = (pos - len(self.intcode)) + 1
            self.intcode.extend([0]*growth)
            self.intcode[pos] = val

    def adjust_relative_base(self, offset):
        self.relative_base += offset

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
            '09': RelativeBaseOp,
            '99': HaltOp
        }
        code = cmd[-2:]
        return opsmap[code]()

    def step(self, pos):
        cmd = str(self.getval(pos, MODE_IMMEDIATE)).zfill(CMD_MAX_SIZE)
        op = self.getop(cmd)
        return op.execute_op(self, cmd, pos)

    def run_program(self, input):
        self.intcode = self.get_intcode()
        self.relative_base = 0
        self.input = iter(input)
        self.output = []

        try:
            pos = 0
            while True:
                pos = self.step(pos)
        except HaltExecutionError:
            pass

        return self.output, self.intcode

    def get_intcode(self):
        return self._intcode[:]


class BaseOp(object):
    # The number of arguments this operation takes
    size = None

    def get_flags(self, cmd):
        start = CMD_MAX_SIZE - 2 - self.size
        return list(cmd[start:start+self.size])[::-1]

    def execute_op(self, intcode, cmd, pos):
        flags = self.get_flags(cmd)

        params = list(enumerate(flags, pos + 1))

        return self.process(intcode, params, pos)

    def process(self, intcode, params, pos):
        self.perform_side_effect(intcode, params)

        return pos + self.size + 1

    def perform_side_effect(self, intcode, params):
        pass


class WriteOp(BaseOp):
    def perform_side_effect(self, intcode, params):
        vals = [
            intcode.getval(pos, mode)
            for (pos, mode) in
            params[:self.size - 1]
        ]

        value = self.calculate(intcode, vals)

        dstPos, dstMode = tuple(params[-1])
        if dstMode == MODE_IMMEDIATE:
            dstMode = MODE_POSITION
        intcode.setval(dstPos, dstMode, value)

    def calculate(self, intcode, vals):
        raise NotImplementedError()


class AddOp(WriteOp):
    size = 3

    def calculate(self, intcode, vals):
        return sum(vals)


class MultiplyOp(WriteOp):
    size = 3

    def calculate(self, intcode, vals):
        valA, valB = vals
        return valA * valB


class LessThanOp(WriteOp):
    size = 3

    def calculate(self, intcode, vals):
        valA, valB = vals
        return 1 if valA < valB else 0


class EqualsOp(WriteOp):
    size = 3

    def calculate(self, intcode, vals):
        valA, valB = vals
        return 1 if valA == valB else 0


class InputOp(WriteOp):
    size = 1

    def calculate(self, intcode, vals):
        return intcode.next_input()


class OutputOp(BaseOp):
    size = 1

    def perform_side_effect(self, intcode, params):
        pos, mode = params[0]
        value = intcode.getval(pos, mode)
        intcode.add_output(value)


class JumpIfTrueOp(BaseOp):
    size = 2

    def process(self, intcode, params, pos):
        vals = [
            intcode.getval(pos, mode)
            for (pos, mode) in
            params
        ]

        if vals[0] != 0:
            return vals[1]
        return super().process(intcode, vals, pos)


class JumpIfFalseOp(BaseOp):
    size = 2

    def process(self, intcode, params, pos):
        vals = [
            intcode.getval(pos, mode)
            for (pos, mode) in
            params
        ]

        if vals[0] == 0:
            return vals[1]
        return super().process(intcode, vals, pos)


class RelativeBaseOp(BaseOp):
    size = 1

    def perform_side_effect(self, intcode, params):
        pos, mode = params[0]
        value = intcode.getval(pos, mode)

        intcode.adjust_relative_base(value)


class HaltOp(BaseOp):
    size = 0

    def perform_side_effect(self, intcode, params):
        raise HaltExecutionError


def test_execution_1():
    machine = Intcode('1,0,0,3,99')

    # Should halt
    machine.run_program([])


def test_execution_2():
    machine = Intcode('1,9,10,3,2,3,11,0,99,30,40,50')

    # Should halt
    machine.run_program([])


def test_execution_3():
    machine = Intcode('1,0,0,0,99')

    _, intcode = machine.run_program([])
    assert intcode == [2, 0, 0, 0, 99]


def test_execution_4():
    machine = Intcode('2,3,0,3,99')

    _, intcode = machine.run_program([])
    assert intcode == [2, 3, 0, 6, 99]


def test_execution_5():
    machine = Intcode('2,4,4,5,99,0')

    _, intcode = machine.run_program([])
    assert intcode == [2, 4, 4, 5, 99, 9801]


def test_execution_6():
    machine = Intcode('1,1,1,4,99,5,6,0,99')

    _, intcode = machine.run_program([])
    assert intcode == [30, 1, 1, 4, 2, 5, 6, 0, 99]


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


def test_quine():
    quine = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    machine = Intcode(quine)

    output, _ = machine.run_program([])
    assert output == machine.get_intcode()


def test_large_output_1():
    machine = Intcode('1102,34915192,34915192,7,4,7,99,0')

    output, _ = machine.run_program([])
    assert output == [1219070632396864]


def test_large_output_2():
    machine = Intcode('104,1125899906842624,99')

    output, _ = machine.run_program([])
    assert output == [1125899906842624]


test_execution_1()
test_execution_2()
test_execution_3()
test_execution_4()
test_execution_5()
test_execution_6()
test_multiply()
test_input_output()
test_negative()
test_equal_pos()
test_less_than_pos()
test_equal_immediate()
test_less_than_immediate()
test_quine()
test_large_output_1()
test_large_output_2()
