from libs.graph_generation.GraphGeneration import Graph

import random

import networkx as nx

class MuscoGraph(Graph):
    """
        Object representing a graph, made with the Musco model.
    """

    def __init__(self, id, nb_nodes, nb_ex, debug_mod = False):
        """
            We call super() to initialize a basic graph with initial properties.
            id : An id to represent the graph
            nb_nodes : An integer to represent the number of nodes in the model
            nb_ex : An integer to represent the number of examples to generate (learning and training)
            debug_mod : A boolean to know if the graph is on debugging mod or not
        """
        super().__init__(id, nb_nodes, nb_ex, debug_mod)

    def generate(self):
        """
            Method to generate the graph based on the Musco model.
            Return a Graph object, based on Musco model - the musco model is available in a scientific paper (see README.md).
        """
        new_graph_vincenzo = nx.DiGraph()

        p = 0.6

        q = 0.4

        all_nodes = [0,1,2]

        all_edges = [(0,1), (0,2)]

        for i in range(3, self.nb_nodes):
            all_nodes.append(i)
            if random.uniform(0,1) <= p:
                random_node = random.choice(all_nodes)
                while random_node == i:
                    random_node = random.choice(all_nodes)
                all_edges.append((i, random_node))
                children = [child for (source, child) in all_edges if (source == random_node)]
                for child in children:
                    all_edges.append((i, child))
                if random.uniform(0,1) <= q:
                    random_node = random.choice(all_nodes)
                    while random_node == i:
                        random_node = random.choice(all_nodes)
                    all_edges.append((i, random_node))
                    children = [child for (source, child) in all_edges if (source == random_node)]
                    for child in children:
                        all_edges.append((i, child))
            else:
                random_node = random.choice(all_nodes)
                while random_node == i:
                    random_node = random.choice(all_nodes)
                all_edges.append((random_node, i))

        new_graph_vincenzo.add_nodes_from(all_nodes)

        new_graph_vincenzo.add_edges_from(all_edges)

        return new_graph_vincenzo
