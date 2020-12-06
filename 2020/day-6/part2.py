from itertools import groupby


def readGroups(data):
    data = (line.strip() for line in data)
    return (group for _, group in groupby(data, lambda v: v == ""))


def readAnswers(data):
    for group in readGroups(data):
        answers = set(next(group))
        for line in group:
            answers &= set(line)
        yield answers


with open("./data.txt", "r") as fp:
    answers = readAnswers(fp.readlines())
    print(sum(len(s) for s in answers))
