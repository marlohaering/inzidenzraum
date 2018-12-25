import numpy as np
import itertools
import timeit
from Line import Line
import networkx as nx
from networkx.algorithms.approximation import min_weighted_dominating_set
from DominationSolver import get_domination_set_approx, draw_graph


def create_graph(n, q):
    tic = timeit.timeit()

    iterators = []
    for i in range(n):
        iterators.append(range(q))

    points = itertools.product(*iterators)
    points = list(map(lambda p: np.array(p), points))

    print('Points generated')

    found_lines = {}
    for p in points:
        found_lines[tuple(p)] = 0

    lines = set()
    for p1 in points:
        for p2 in points:
            if tuple(p1) != tuple(p2):
                l = Line(p1, p2, q)
                new_line_added = l not in lines
                lines.add(l)
                if new_line_added:
                    found_lines[tuple(p1)] += 1
                    found_lines[tuple(p2)] += 1

    print('Lines generarted')

    V = points + list(lines)

    E = []

    for l in lines:
        for p in l.points:
            if l.is_on_line(p):
                E.append((p, l))

    toc = timeit.timeit()

    # [print(str(v)) for v in V]  # print nodes
    [print(str(p)) for p in points]  # print points
    [print(l.p1, l.p2, str(l)) for l in lines]  # print lines

    [print(str(v1), str(v2)) for v1, v2 in E]  # print edges

    print('#points', len(points))
    print('#lines', len(lines))
    print('#nodes', len(V))
    print('#edges', len(E))

    # print(found_lines)

    G = nx.Graph()
    for v1, v2 in E:
        G.add_edge(v1, v2)

    # p1 = np.array([0, 0, 0])
    # p2 = np.array([0, 0, 3])
    # p3 = np.array([0, 2, 1])
    #
    # print(p1)
    # print(p2)
    #
    # line = Line(p1, p2)
    # line2 = Line(p1, p3)
    # print(line)
    # print(line2)
    #
    # print(line == line2)

    return G


if __name__ == '__main__':
    n = 2
    q = 3

    G = create_graph(n, q)
    # domination_set = min_weighted_dominating_set(G)
    domination_set2 = get_domination_set_approx(G)
    # print('domination_set: ', [str(node) for node in domination_set])
    print('domination_set2: ', [str(node) for node in domination_set2])
    # print('#nodes: ', len(domination_set))
    print('#nodes2: ', len(domination_set2))

    # draw_graph(G)
#