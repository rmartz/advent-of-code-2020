def remove_paired_letters(line):
    index = 0
    while index < len(line) - 1:
        a, b = line[index:index + 2]
        if a != b and a.lower() == b.lower():
            line = line[:index] + line[index + 2:]
            changed = True
            index = max(index - 1, 0)
        else:
            index += 1
    return line

with open('data.txt', 'r') as fp:
    line = fp.readline()

print(len(remove_paired_letters(line)))
