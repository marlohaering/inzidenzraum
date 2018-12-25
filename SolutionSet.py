import operator

import networkx as nx


class SolutionSet(object):
    def __init__(self, s, t, graph, radius):
        self.S = s
        self.T = t
        self.G = graph
        self.W_values = {}
        self.radius = radius
        self.refresh_w_values()

    def refresh_w_values(self):
        for n in set(self.G.nodes()):
            if n not in self.T:
                self.W_values[n] = self.get_w_value(n)
            else:
                if n in self.W_values:
                    self.W_values.pop(n)

    def add_t(self, node):
        self.T.add(node)
        self.refresh_w_values()

    def add_s(self, node):
        self.S.add(node)
        self.refresh_w_values()

    def get_max_w_value(self):
        return max(self.W_values.values())

    def get_node_max_w_value(self):
        return max(self.W_values.items(), key=operator.itemgetter(1))[0]

    def get_covered_nodes(self):
        covered_nodes = set()
        for node in self.S:
            covered_nodes.update(self.get_ball(node, self.radius))
        return covered_nodes

        return nodes

    def get_ball(self, node, radius):
        # nodes = set()
        # nodes.add(node)
        # nodes.update(self.G.neighbors(node))
        # return nodes

        return set([node] + list(self.G.neighbors(node)))  # For radius = 1


        # nodes = set()
        # nodes.add(node)
        #
        # path_lengths = nx.single_source_dijkstra_path_length(self.G, node)
        # nodes.update([node for node, length in path_lengths.items()
        #               if length <= radius])
        # return nodes

    def get_uncovered_nodes(self):
        return set(self.G.nodes()) - self.get_covered_nodes()

    def get_w_value(self, node):
        return len(self.get_ball(node, self.radius) - self.get_covered_nodes())

    def get_lower_bound(self):
        if self.get_max_w_value() != 0:
            return len(self.S) + len(self.get_uncovered_nodes()) / self.get_max_w_value()
        return None

    def __str__(self):
        return f'S: {str(self.S)} T: {str(self.T)} Highest node: {self.get_node_max_w_value()} Lower bound: {self.get_lower_bound()}'
