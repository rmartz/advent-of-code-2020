from collections import namedtuple

Instruction = namedtuple("Instruction", ["cmd", "args"])
State = namedtuple("State", ["pc", "acc"])


class GameCodeInterpreter(object):
    state = None
    instructions = None

    def __init__(self, instructions):
        self.state = State(pc=0, acc=0)
        self.instructions = list(instructions)

    def step(self):
        instruction = self.instructions[self.state.pc]
        self.state = self.process(self.state, instruction)
        return self.state

    @staticmethod
    def process(state, instruction):
        instructions = {
            "acc": lambda: State(
                pc=state.pc + 1, acc=state.acc + int(instruction.args[0])
            ),
            "nop": lambda: State(pc=state.pc + 1, acc=state.acc),
            "jmp": lambda: State(pc=state.pc + int(instruction.args[0]), acc=state.acc),
        }
        return instructions[instruction.cmd]()


def lineToInstruction(line):
    cmd, *args = line.split(" ")
    return Instruction(cmd=cmd, args=args)


def generateCorruptions(instructions):
    swaps = {"nop": "jmp", "jmp": "nop"}

    for i, instruction in enumerate(instructions):
        if instruction.cmd not in swaps:
            continue

        copy = instructions[:]
        newCmd = swaps[instruction.cmd]
        copy[i] = Instruction(cmd=newCmd, args=instruction.args)
        yield copy


def checkTermination(instructions):
    gci = GameCodeInterpreter(instructions)

    visittedLines = set()
    state = gci.state
    while state.pc not in visittedLines:
        visittedLines.add(state.pc)
        try:
            state = gci.step()
        except IndexError:
            return state.acc
    else:
        return None


with open("./data.txt", "r") as fp:
    source = list(lineToInstruction(line) for line in fp)

for instructions in generateCorruptions(source):
    acc = checkTermination(instructions)
    if acc is None:
        continue
    print(acc)
    break
