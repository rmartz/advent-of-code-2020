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

def find_shortest_processed_lines(line):
    elements = '0abcdefghijklmnopqrstuvwxyz'
    for elem in elements:
        stripped_string = ''.join(l for l in line if l.lower() != elem)
        yield len(remove_paired_letters(stripped_string))


with open('data.txt', 'r') as fp:
    line = fp.readline()

print(min(find_shortest_processed_lines(line)))
