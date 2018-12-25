import networkx as ng
from networkx.algorithms.bipartite import gnmk_random_graph
from networkx.generators import *

from DominationSolver import draw_graph

if __name__ == '__main__':
    G = gnmk_random_graph(5,5, 20)

    draw_graph(G)