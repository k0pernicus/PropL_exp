from libs.utils.utils import isEmpty

import random

import networkx as nx

class Graph(object):
    """
    Object to represent a graph.
    A graph is a representation of a network of nodes, join by edges.
    This structure contains some methods to analyse accurately this one and to do machine learning on it.
    """

    def __init__(self, id, nb_nodes, nb_ex, debug_mod):
        self.debug_mod = debug_mod
        self.id = id
        self.nb_nodes = nb_nodes
        self.nb_ex = nb_ex
        self.init_nodes = []
        self.weights_matrix = {}
        self.graph = self.generate()
        if self.debug_mod :
            print("Graph {} created!".format(self.id))

    def __del__(self):
        print("Graph {} has been deleted.".format(self.id))

    def run(self):
        self.putLabelsAndInitWeightsMatrix()
        self.init_nodes = self.computeInitNodes()
        self.computeWeightsMatrix()

    def generate(self):
        """
        Abstract: Function to generate a graph like Vincenzo Musco works
        """
        pass

    def putLabelsAndInitWeightsMatrix(self):
        """
        Abstract: Primitive to label a node, in the self.graph parameter
        """

        for source_node in self.graph.nodes():

            self.weights_matrix[source_node] = {}
            self.weights_matrix[source_node]['visited'] = False

            #add label "target" to each node which is a target of an edge AND which is not already a source
            if len(self.graph.edge[source_node]) == 0:
                self.graph.node[source_node] = "target"

            else:
                #add label "source" to each node which is a source of an edge
                self.graph.node[source_node] = "source"

                nb_of_target_nodes = len(self.graph.edge[source_node])

                self.weights_matrix[source_node][source_node] = 0

                #for each target_node, put the probability to go in the next node to 1/nb_of_target_nodes
                for target_node in self.graph.edge[source_node]:
                    self.weights_matrix[source_node][target_node] = 1/nb_of_target_nodes

    def computeInitNodes(self):
        """
        Abstract: Function to return init nodes in the graph
        """

        init_nodes = []

        for i in range(0, self.nb_nodes):
            init_nodes.append(i)

        #for each target of each edge, replace the number by 0
        for edge in self.graph.edges():
            #avoid recursive functions
            if edge[0] != edge[1]:
                init_nodes[edge[1]] = -1

        if self.debug_mod:
            print("Init nodes are : {}".format(init_nodes))

        return [x for x in init_nodes if x != -1 and len(self.graph.edge[x]) != 0]

    def computeSpecificWeight(self, probability_of_source_edge, source_node, target_node):
        """
        Abstract: Primitive to compute the weight of edges, based on his own propagation probability
        """

        is_target_node_visited = self.weights_matrix[target_node]['visited']

        if self.debug_mod:
            print("target {0} visited -> {1}".format(target_node, is_target_node_visited))

        if is_target_node_visited:
            self.weights_matrix[source_node][target_node] = (self.weights_matrix[source_node][target_node] + probability_of_source_edge) / 2
        else:
            self.weights_matrix[source_node][target_node] = self.weights_matrix[source_node][target_node] * probability_of_source_edge
            self.weights_matrix[target_node]['visited'] = True

    def computeWeightsMatrix(self):
        """
        Abstract: Primitive to compute the weights matrix
        """

        if self.debug_mod:
            print("Edges are {}".format(self.graph.edges()))

        #for each init node in all init nodes...
        for init_node in self.init_nodes:

            if self.debug_mod:
                print("Init node : {}".format(init_node))

            #we create an array which contains visited nodes
            visited_nodes = [init_node]

            #we create an array which contains nodes to visit
            nodes_stack = []

            #iteration on target nodes, from init node
            for target_node in self.graph.edge[init_node]:

                if (self.graph.node[target_node] != "target"):

                    nodes_stack.append((target_node, self.weights_matrix[init_node][target_node]))

            while not isEmpty(nodes_stack):

                source_node, probability_to_propagate_between_source_target = nodes_stack.pop()

                if self.debug_mod:
                    print("Target node : {}".format(source_node))

                probability_to_propagate_from_source_node = 0

                for target_node in self.graph.edge[source_node]:

                    if self.debug_mod:
                        print("\t...source node {}".format(target_node))

                    if source_node != target_node:

                        self.computeSpecificWeight(probability_to_propagate_between_source_target, source_node, target_node)

                        probability_to_propagate_from_source_node += self.weights_matrix[source_node][target_node]

                        if (not target_node in nodes_stack) and (not target_node in visited_nodes):

                            if self.debug_mod:
                                print("\t\t... {} added".format(target_node))

                            nodes_stack.append((target_node, self.weights_matrix[source_node][target_node]))

                self.weights_matrix[init_node][source_node] = probability_to_propagate_from_source_node

                self.weights_matrix[init_node][init_node] = 1 - probability_to_propagate_from_source_node
