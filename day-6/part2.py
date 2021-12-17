from itertools import groupby


def readGroups(data):
    data = (line.strip() for line in data)
    return (group for isBlank, group in groupby(data, lambda v: v == "") if not isBlank)


def readAnswers(data):
    for group in readGroups(data):
        answers = set(next(group))
        for line in group:
            answers &= set(line)
        yield answers


with open("./data.txt", "r") as fp:
    answers = readAnswers(fp.readlines())
    print(sum(len(s) for s in answers))
