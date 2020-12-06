def read_value(input):
    return int(next(input))


def read_node(input):
    count_children = read_value(input)
    count_metadata = read_value(input)

    total = 0
    for i in range(count_children):
        total += read_node(input)

    for i in range(count_metadata):
        total += read_value(input)

    return total


with open("data.txt", "r") as fp:
    data = fp.read().split(" ")

print(read_node(iter(data)))
