

def readAnswers(data):
    answers = None
    for line in data:
        line = line.strip()
        if line == "":
            yield answers
            answers = None
        elif answers is None:
            answers = set(line)
        else:
            answers &= set(line)
    if answers:
        yield answers


with open("./data.txt", "r") as fp:
    answers = readAnswers(fp.readlines())
    print(sum(len(s) for s in answers))
