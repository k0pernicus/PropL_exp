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

                if not edge[1] in self.get_sources_for_target:
                    self.get_sources_for_target[edge[1]] = []

                self.get_sources_for_target[edge[1]].append(edge[0])

        if self.debug_mod:
            print("Init nodes are : {}".format(init_nodes))

        self.init_nodes = [x for x in init_nodes if x != -1 and len(self.graph.edge[x]) != 0]

    def computeSpecificWeight(self, source_node, target_node, local_probability_to_come):
        """
            Method to compute a specific weight between two nodes ('source_node' and 'target_node'), with the probability to come in this state ('local_probability_to_come')
        """

        self.weights_matrix[source_node][target_node] = round(self.weights_matrix[source_node][target_node] * local_probability_to_come,3)

    def computeFinalNodesForSourceNodes(self):
        """
            Method to compute 'final' nodes accessible for each node.
        """

        for final_node in self.final_nodes:

            visited_nodes = []

            source_nodes_stack = []

            for source_node in self.get_sources_for_target[final_node]:

                source_nodes_stack.append(source_node)

            while not isEmpty(source_nodes_stack):

                local_source_node = source_nodes_stack.pop()

                visited_nodes.append(local_source_node)

                if not local_source_node in self.final_nodes_for_source_node:
                    self.final_nodes_for_source_node[local_source_node] = []

                if not final_node in self.final_nodes_for_source_node[local_source_node]:
                    self.final_nodes_for_source_node[local_source_node].append(final_node)

                if not local_source_node in self.init_nodes:
                    for next_source_node in self.get_sources_for_target[local_source_node]:

                        if (not next_source_node in visited_nodes) and (not next_source_node in source_nodes_stack):
                            source_nodes_stack.append(next_source_node)
