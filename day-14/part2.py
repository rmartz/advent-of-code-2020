from collections import namedtuple
from enum import Enum
from functools import reduce


class Commands(Enum):
    Mask = "mask"
    Mem = "mem"


State = namedtuple("State", ["mask", "registers"])
Instruction = namedtuple("Instruction", ["cmd", "arg", "val"])


def update_mask(state, mask):
    return State(mask=mask, registers=state.registers)


def write_memory(state, address, value):
    registers = state.registers.copy()
    for mask in mask_permutations(state.mask):
        registers[apply_mask(mask, address)] = value
    return State(mask=state.mask, registers=registers)


def mask_permutations(mask):
    prefix = ""
    for i, c in enumerate(mask):
        # 0 is the new "unchanged"
        if c == "0":
            prefix += "X"
        # 1 means set to 1
        elif c == "1":
            prefix += "1"
        # X means both set to 1 and 0
        if c == "X":
            remainder = mask[i + 1 :]
            for suffix in mask_permutations(remainder):
                yield prefix + "0" + suffix
                yield prefix + "1" + suffix
            return
    yield prefix


def apply_mask(mask, value):
    # Create a bitmask that is 1 in all cases unless the corresponding character is a 0
    and_mask = reduce(lambda m, c: (m << 1) | (c != "0"), mask, 0)

    # Create a bitmask that is 0 in all cases unless the corresponding character is a 1
    or_mask = reduce(lambda m, c: (m << 1) | (c == "1"), mask, 0)

    return value & and_mask | or_mask


def process_state(state, instruction):
    if instruction.cmd == Commands.Mask:
        return update_mask(state, instruction.val)
    return write_memory(state, instruction.arg, instruction.val)


def parse_input(line):
    cmd, val = line.strip().split(" = ")
    if cmd == "mask":
        return Instruction(cmd=Commands(cmd), val=val, arg=None)
    cmd, arg = cmd.split("[")
    arg = arg[:-1]

    return Instruction(cmd=Commands(cmd), val=int(val), arg=int(arg))


with open("./data.txt", "r") as fp:
    instructions = (parse_input(line) for line in fp)
    state = reduce(process_state, instructions, State(mask="", registers={}))

print(sum(state.registers.values()))
