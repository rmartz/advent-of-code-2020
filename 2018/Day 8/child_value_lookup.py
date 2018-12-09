def read_value(input):
    return int(next(input))

def read_node(input):
    count_children = read_value(input)
    count_metadata = read_value(input)

    child_values = {}
    for i in range(count_children):
        child_values[i] = read_node(input)

    total = 0
    if count_children == 0:
        for i in range(count_metadata):
            total += read_value(input)
    else:
        for i in range(count_metadata):
            index = read_value(input)
            total += child_values.get(index - 1, 0)


    return total

with open('data.txt', 'r') as fp:
    data = fp.read().split(' ')

print(read_node(iter(data)))