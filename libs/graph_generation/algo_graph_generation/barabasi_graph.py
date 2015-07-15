from libs.graph_generation.graph_generation import Graph

import networkx as nx

class BarabasiGraph(Graph):
    """
        Object representing a graph, made with the Barabasi-Albert model.
    """

    def __init__(self, id, nb_nodes, degree, nb_ex, debug_mod = False):
        """
            We call super() to initialize a basic graph with initial properties.
            id : An id to represent the graph
            nb_nodes : An integer to represent the number of nodes in the model
            degree : An integer to represent the average degree of each node in the model
            nb_ex : An integer to represent the number of examples to generate (learning and training)
            debug_mod : A boolean to know if the graph is on debugging mod or not
            Note : We add the degree field because the generation of the graph, with the Barabasi-Albert model, needs this one - it's not important for other graphs models (like the Musco model).
        """
        self.degree = degree
        super().__init__(id, nb_nodes, nb_ex, debug_mod)

    def generate(self):
        """
            Method to generate the graph based on the Barabasi-Albert model.
            Return a Graph object, based on Barabasi-Albert model.
        """
        return nx.barabasi_albert_graph(self.nb_nodes, self.degree)
