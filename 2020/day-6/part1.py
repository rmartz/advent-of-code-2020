from itertools import groupby


def readGroups(data):
    return (
        (v.strip() for v in group)
        for _, group in groupby(data, lambda v: v.strip() == "")
    )


def readAnswers(data):
    for group in readGroups(data):
        answers = set()
        for line in group:
            answers |= set(line)
        yield answers


with open("./data.txt", "r") as fp:
    answers = readAnswers(fp.readlines())

    print(sum(len(s) for s in answers))
