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
    registers[address] = apply_mask(state.mask, value)
    return State(mask=state.mask, registers=registers)


def apply_mask(mask, value):
    # Create a bitmask that is 1 in all cases unless the corresponding character is a 0
    and_mask = reduce(lambda m, c: (m << 1) | (c != "0"), mask, 0)

    # Create a bitmask that is 0 in all cases unless the corresponding character is a 1
    or_mask = reduce(lambda m, c: (m << 1) | (c == "1"), mask, 0)

    return int(value) & and_mask | or_mask


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

    return Instruction(cmd=Commands(cmd), val=val, arg=arg)


with open("./data.txt", "r") as fp:
    instructions = (parse_input(line) for line in fp)
    state = reduce(process_state, instructions, State(mask="", registers={}))

print(sum(state.registers.values()))
