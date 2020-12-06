with open("data.txt", "r") as fp:
    values = list(int(row) for row in fp)

sums = set()

total = 0
while True:
    for v in values:
        total += v
        if total in sums:
            print(total)
            exit()
        sums.add(total)
