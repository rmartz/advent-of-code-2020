from collections import namedtuple, defaultdict
import re

INPUT_REGEX = re.compile("([a-z]+) contains ([0-9]+ ([a-z]+))")
WeightedDirectedEdge = namedtuple("DirectedEdge", ["source", "target", "weight"])


def inputToVertices(lines):
    for line in lines:
        line = line.strip(" .\n")
        yield from lineToVertices(line)


def lineToVertices(line):
    source, targets = line.split(" contain ")
    for target in targets.split(", "):
        count, color = target.split(" ", 1)
        count = 0 if count == "no" else int(count)
        yield WeightedDirectedEdge(
            source=colorName(source), target=colorName(color), weight=count
        )


def colorName(bags):
    return " ".join(bags.split(" ")[:-1])


def verticesToDirectedGraph(vertices):
    graph = defaultdict(set)
    for vertex in vertices:
        graph[vertex.source].add(vertex)

    return graph


def findTotalNodeWeight(vertices, node):
    graph = verticesToDirectedGraph(vertices)

    return findNodeWeight(graph, graph[node]) - 1


def findNodeWeight(graph, connections):
    weight = 1
    for connection in connections:
        subConnections = graph[connection.target]
        weight += connection.weight * findNodeWeight(graph, subConnections)
    return weight


TARGET_COLOR = "shiny gold"

with open("./data.txt", "r") as fp:
    vertices = inputToVertices(fp)
    print(findTotalNodeWeight(vertices, TARGET_COLOR))
