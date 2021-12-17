from collections import namedtuple


SeatPos = namedtuple("SeatPos", ["row", "col"])
Statistics = namedtuple("Statistics", ["total", "max", "min"])


class BinarySearch(object):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def current(self):
        return int((self.low + self.high) / 2)

    def lower(self):
        self.high = self.current()

    def higher(self):
        self.low = self.current() + 1


def BinarySpaceLookup(code, low, high, upper):
    bs = BinarySearch(low, high)
    for c in code:
        if c == upper:
            bs.higher()
        else:
            bs.lower()
    return bs.current()


def GetSeatPos(seatcode):
    row_code = seatcode[0:7]
    col_code = seatcode[7:10]
    return SeatPos(
        row=BinarySpaceLookup(row_code, 0, 127, "B"),
        col=BinarySpaceLookup(col_code, 0, 7, "R"),
    )


def GetSeatId(seatpos: SeatPos):
    return seatpos.row * 8 + seatpos.col


def CollectStatistics(numbers):
    low = high = total = next(numbers)
    for n in numbers:
        total += n
        low = min(low, n)
        high = max(high, n)

    return Statistics(total=total, min=low, max=high)


def TotalSequentialDigits(n):
    return n * (n + 1) / 2


def TotalSequentialDigitRange(low, high):
    return TotalSequentialDigits(high) - TotalSequentialDigits(low - 1)


assert GetSeatPos("FBFBBFFRLR") == SeatPos(row=44, col=5)

assert GetSeatPos("BFFFBBFRRR") == SeatPos(row=70, col=7)
assert GetSeatId(SeatPos(row=70, col=7)) == 567

assert GetSeatPos("FFFBBBFRRR") == SeatPos(row=14, col=7)
assert GetSeatId(SeatPos(row=14, col=7)) == 119

assert GetSeatPos("BBFFBBFRLL") == SeatPos(row=102, col=4)
assert GetSeatId(SeatPos(row=102, col=4)) == 820

with open("./data.txt", "r") as fp:
    seat_positions = (GetSeatPos(code) for code in fp.readlines())
    ids = (GetSeatId(pos) for pos in seat_positions)
    stats = CollectStatistics(ids)

expected_total = TotalSequentialDigitRange(stats.min, stats.max)
seat = expected_total - stats.total
print(seat)
