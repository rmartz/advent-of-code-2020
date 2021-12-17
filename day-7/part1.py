from collections import namedtuple, defaultdict
import re

INPUT_REGEX = re.compile("([a-z]+) contains ([0-9]+ ([a-z]+))")
DirectedEdge = namedtuple("DirectedEdge", ["source", "target"])


def inputToVertices(lines):
    for line in lines:
        line = line.strip(" .\n")
        yield from lineToVertices(line)


def lineToVertices(line):
    source, targets = line.split(" contain ")
    for target in targets.split(", "):
        count, color = target.split(" ", 1)
        yield DirectedEdge(source=colorName(source), target=colorName(color))


def colorName(bags):
    return " ".join(bags.split(" ")[:-1])


def verticesToReachabilityGraph(vertices):
    reachableFrom = defaultdict(set)
    for vertex in vertices:
        reachableFrom[vertex.target].add(vertex.source)

    return reachableFrom


def findAllConnectedSources(vertices, target):
    graph = verticesToReachabilityGraph(vertices)

    toProcess = list([target])
    results = set()

    while toProcess:
        source = toProcess.pop()
        newResults = graph[source] - results
        results |= newResults
        toProcess.extend(list(newResults))

    return results


TARGET_COLOR = "shiny gold"

with open("./data.txt", "r") as fp:
    vertices = inputToVertices(fp)
    print(len(findAllConnectedSources(vertices, TARGET_COLOR)))
