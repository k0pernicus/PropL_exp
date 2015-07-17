from libs.graph_generation.GraphGeneration import Graph

import networkx as nx

from networkx import is_directed_acyclic_graph

class BarabasiGraph(Graph):
    """
        Object representing a graph, made with the Barabasi-Albert model.
    """

    def __init__(self, id, nb_nodes, degree, nb_ex, nb_split_ex = 10, method="uniform", debug_mod = False):
        """
            We call super() to initialize a basic graph with initial properties.
            id : An id to represent the graph
            nb_nodes : An integer to represent the number of nodes in the model
            degree : An integer to represent the average degree of each node in the model
            nb_ex : An integer to represent the number of examples to generate (learning and training)
            method : A string which represents the method used to generate probabilities ("unform", "random")
            debug_mod : A boolean to know if the graph is on debugging mod or not
            Note : We add the degree field because the generation of the graph, with the Barabasi-Albert model, needs this one - it's not important for other graphs models (like the Musco model).
        """
        self.degree = degree
        super().__init__(id, nb_nodes, nb_ex, nb_split_ex, method, debug_mod)

    def generate(self):
        """
            Method to generate the graph based on the Barabasi-Albert model.
            Return a Graph object, based on Barabasi-Albert model (directed graph).
        """
        #Creation of a directed graph
        g = nx.DiGraph()

        #we return the graph (new_graph_vincenzo) if he's not acyclic and directed
        while True:
            #Creation of a graph from Barabasi-Albert model
            b = nx.barabasi_albert_graph(self.nb_nodes, self.degree)
            #Add all nodes and edges from b to g (because g canno't be directed by NetworkX)
            g.add_nodes_from(b.nodes())
            g.add_edges_from(b.edges())

            if is_directed_acyclic_graph(g):
                break
            else:
                #new digraph to continue...
                g = nx.DiGraph()

        #Finally, return the directed graph
        return g
