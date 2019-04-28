import operator
import random
from pprint import pprint
import matplotlib.pyplot as plt

import networkx as nx
from networkx.drawing.nx_pylab import draw
from SolutionSet import SolutionSet
import copy

solution_bounds = {}
depth = 1


def createGraph(edges: str):
    """
    Creates a graph from string
    :param edges: format: node<SPACE>node
    :return: Graph
    """
    lines = edges.split('\n')
    G = nx.Graph()
    for line in lines:
        node1, node2 = line.split()
        G.add_edge(node1, node2)
    return G


def createGaph1():
    G = nx.Graph()
    for i in range(29):
        G.add_edge(str(i+1), str(i+2))
    G.add_edge('30', '1')
    
    G.add_edge('1', '10')
    G.add_edge('2', '15')
    G.add_edge('3', '20')
    G.add_edge('4', '25')
    G.add_edge('5', '12')
    G.add_edge('6', '29')
    G.add_edge('7', '16')
    G.add_edge('8', '21')
    G.add_edge('9', '26')
    G.add_edge('10', '1')
    G.add_edge('11', '18')
    G.add_edge('12', '5')
    G.add_edge('13', '22')
    G.add_edge('14', '27')

    return G


def createGaph2():
    G = nx.Graph()
    G.add_edge('a', 'b')
    G.add_edge('c', 'd')
    G.add_edge('d', 'b')
    G.add_edge('b', 'e')
    G.add_edge('b', 'h')
    G.add_edge('d', 'g')
    G.add_edge('c', 'f')
    G.add_edge('c', 'i')
    G.add_edge('d', 'h')
    G.add_edge('f', 'i')
    G.add_edge('h', 'j')
    G.add_edge('e', 'k')
    G.add_edge('l', 'j')
    G.add_edge('i', 'l')
    G.add_edge('k', 'n')
    G.add_edge('k', 'm')
    G.add_edge('j', 'k')
    G.add_edge('l', 'm')
    G.add_edge('l', 'o')
    G.add_edge('m', 'p')
    G.add_edge('n', 'p')
    G.add_edge('n', 'q')
    G.add_edge('o', 'p')
    G.add_edge('p', 'q')

    return G


def try_next_solution():
    global depth
    # print('Depth: ', depth)
    depth += 1
    if None not in solution_bounds.values():
        solution = min(solution_bounds.items(), key=operator.itemgetter(1))[0]
        highest_w_node = solution.get_node_max_w_value()
        solution_with_node = copy.deepcopy(solution)
        solution_without_node = copy.deepcopy(solution)
        solution_with_node.add_s(highest_w_node)
        solution_without_node.add_t(highest_w_node)

        x1 = solution_with_node.get_uncovered_nodes()
        if len(x1) == 0:
            return solution_with_node
        x2 = solution_without_node.get_uncovered_nodes()
        if len(x2) == 0:
            return solution_without_node

        solution_bounds[solution_with_node] = solution_with_node.get_lower_bound()
        solution_bounds[solution_without_node] = solution_without_node.get_lower_bound(
        )

        # print(solution_with_node)
        # print(solution_without_node)

        solution_bounds.pop(solution)

    return -1


def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges,
                           width=6)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    plt.show()


def get_domination_set_approx(G):
    solution_set = SolutionSet(set(), set(), G, 1)
    mv = max(solution_set.W_values.values())
    max_node = random.choice(
        [k for (k, v) in solution_set.W_values.items() if v == mv])

    while solution_set.W_values[max_node] > 0:
        print('Added: ', max_node)
        solution_set.add_s(max_node)

        mv = max(solution_set.W_values.values())
        max_node = random.choice(
            [k for (k, v) in solution_set.W_values.items() if v == mv])

    return solution_set.S


def get_domination_set(G, radius=1):
    S = set()
    T = set()
    solutionSet = SolutionSet(S, T, G, radius)
    solution_bounds[solutionSet] = solutionSet.get_lower_bound()
    solution_found = try_next_solution()

    while solution_found == -1:
        solution_found = try_next_solution()

    # pprint(solution_bounds)

    return solution_found.S


if __name__ == '__main__':
    G = createGaph1()
    domination_set = get_domination_set(G)
    print('domination_set: ', [str(node) for node in domination_set])
    print('#nodes: ', len(domination_set))

    # draw_graph(G)
