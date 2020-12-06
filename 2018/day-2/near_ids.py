from itertools import count


def remove_at(value, index):
    return value[:index] + value[index + 1 :]


with open("data.txt", "r") as fp:
    ids = list(fp)

for index in count():
    keys = set()
    items = ((remove_at(val, index), val) for val in ids)
    for key, val in items:
        if key in keys:
            print(key)
            exit()
        keys.add(key)
