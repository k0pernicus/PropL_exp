from libs.utils.utils import isEmpty
from libs.utils.utils import chunksList

from libs.learning_and_testing_lib.learning.Learning import LearningSet
from libs.learning_and_testing_lib.testing.Testing import TestingSet

import random

import networkx as nx

class Graph(object):
    """
        Object to represent a graph.
        A graph is a representation of a network of nodes, join by edges.
        We suppose our graphs are directed and acyclics.
        This structure contains some methods to analyse accurately this one and to do machine learning on it.
        id : An id to represent the graph
        nb_nodes : An integer to represent the number of nodes in the model
        nb_ex : An integer to represent the number of examples to generate (learning and training)
        method : A string which represents the method used to generate probabilities ("unform", "random")
        debug_mod : A boolean to know if the graph is on debugging mod or not
    """

    def __init__(self, id, nb_nodes, nb_ex, nb_split_ex, method, debug_mod = True):
        self.debug_mod = debug_mod
        self.id = id
        self.nb_nodes = nb_nodes
        self.nb_ex = nb_ex
        self.nb_split_ex = nb_split_ex
        self.init_nodes = []
        self.final_nodes = []
        self.weights_matrix = {}
        self.final_nodes_for_source_node = {}
        self.get_sources_for_target = {}
        self.graph = self.generate()
        self.method = method
        if self.debug_mod :
            print("Graph {} created!".format(self.id))

    def __del__(self):
        print("Graph {0} has been deleted.".format(self.id))

    def run(self):
        """
            Default method to put labels like 'source' (a 'source' node is a node which have a target), or 'final' (a 'final' node is a node which not have a target).
            This method computes also 'init' nodes (an 'init' node is a node which is not a target).
        """
        self.computeInitNodesAndSourcesForATarget()
        if self.method == "uniform":
            self.putLabelsAndInitWeightsMatrixUNIFORM()
        if self.method == "random":
            self.putLabelsAndInitWeightsMatrixRANDOM()
        self.computeFinalNodesForSourceNodes()

    def generate(self):
        """
            Default method to generate the wished graph.
        """

        pass

    def generatePropagationFrom(self, source_node):
        """
            Method to generate a bug propagation from 'source_node'
        """

        impacted_nodes = []

        impacted_nodes_stack = []

        impacted_nodes_stack.append(source_node)

        #The algorithm is simple.
        #1. We create a stack which contains all visited nodes.
        #2. For each target of the visited node, we check if a random number is <= at the value of the edge between the visited node and the current target.
        #3. Then (if yes), we add the target_node object to the list of impacted nodes, else : Game Over (for the current target).
        #4. Return the array which contains visited nodes.
        while not isEmpty(impacted_nodes_stack):

            local_source_node = impacted_nodes_stack.pop()

            for target_node in self.graph.edge[local_source_node]:
                random_gen = random.uniform(0, 1)
                if random_gen <= self.weights_matrix[local_source_node][target_node]:
                    impacted_nodes.append(target_node)
                    impacted_nodes_stack.append(target_node)

        return impacted_nodes

    def generateExamples(self):
        """
            Default method to generate some usefull examples.
            These examples belongs to the (learning + test) data set.
            This method returns a couple of objects : a Learning object (contains data set to learn) and a Testing object (contains data set to test)
        """

        #Data set for learning and testing ex
        learning_and_testing_set = []

        #Arbitrary value
        source_node = 0

        for i in range(0, self.nb_ex):
            #Take a random node (!= target)
            while True:
                source_node = random.choice(self.graph.nodes())
                if self.graph.node[source_node] != "final":
                    break
                continue
            #Get the list of impacted nodes
            impacted_nodes = self.generatePropagationFrom(source_node)
            th_final_nodes = self.final_nodes_for_source_node[source_node]
            #Get the list of impacted final nodes
            impacted_final_nodes = [x for x in impacted_nodes if x in th_final_nodes]
            #Add in the global structure the couple source_node, impacted_final_nodes
            learning_and_testing_set.append((source_node, impacted_final_nodes))

        #chunk the list
        chunked_list = chunksList(learning_and_testing_set, 2 * round(len(learning_and_testing_set) / self.nb_split_ex))

        #pop a random sublist - this sublist become the testing set.
        set_for_tests = chunked_list.pop(chunked_list.index(random.choice(chunked_list)))

        #At this point, chunked_list is the list of learning tests

        #Learning and Testing objects
        learning_set = LearningSet("learning_set", self.id, [test for tests in chunked_list for test in tests], self.debug_mod)
        testing_set = TestingSet("testing set", self.id, set_for_tests, self.debug_mod)

        return learning_set, testing_set

    def putLabelsAndInitWeightsMatrixUNIFORM(self):
        """
            Method to put labels like 'source' (a 'source' node is a node which have a target), or 'final' (a 'final' node is a node which not have a target), on each node in the graph.
            Uniform approach : each target node have the same probability of his neighbors.
        """

        for source_node in self.graph.nodes():

            self.weights_matrix[source_node] = {}

            #add label "target" to each node which is a target of an edge AND which is not already a source
            if len(self.graph.edge[source_node]) == 0:
                self.graph.node[source_node] = "final"
                self.final_nodes.append(source_node)

            else:
                #add label "source" to each node which is a source of an edge
                self.graph.node[source_node] = "source"

                nb_of_target_nodes = len(self.graph.edge[source_node])

                #if it's not recursive, we add the source_node as a target of himself
                if not source_node in self.graph.edge[source_node]:

                    weight_to_add = round(1/ (nb_of_target_nodes + 1), 3)

                    #for each target_node, put the probability to go in the next node to 1/nb_of_target_nodes
                    for target_node in self.graph.edge[source_node]:
                        self.weights_matrix[source_node][target_node] = weight_to_add

                    self.weights_matrix[source_node][source_node] = weight_to_add

                #else, everything is ok...
                else:
                    weight_to_add = round(1 / nb_of_target_nodes, 3)

                    for target_node in self.graph.edge[source_node]:
                        self.weights_matrix[source_node][target_node] = weight_to_add

    def putLabelsAndInitWeightsMatrixRANDOM(self):
        """
            Method to put labels like 'source' (a 'source' node is a node which have a target), or 'final' (a 'final' node is a node which not have a target), on each node in the graph.
            Random approach : The probability of a target is random. The sum of his weight + neighbors's weight = 1.
        """

        for source_node in self.graph.nodes():

            self.weights_matrix[source_node] = {}

            #add label "target" to each node which is a target of an edge AND which is not already a source
            if len(self.graph.edge[source_node]) == 0:
                self.graph.node[source_node] = "final"
                self.final_nodes.append(source_node)

            else:
                #add label "source" to each node which is a source of an edge
                self.graph.node[source_node] = "source"

                nb_of_target_nodes = len(self.graph.edge[source_node])

                #if it's not recursive, we add the source_node as a target of himself
                if not source_node in self.graph.edge[source_node]:

                    total_weight = 1

                    #for each target_node, put the probability to go in the next node to 1/nb_of_target_nodes
                    for target_node in self.graph.edge[source_node]:
                        if target_node != source_node:
                            weight_to_add = round(random.uniform(0,total_weight), 3)
                            self.weights_matrix[source_node][target_node] = weight_to_add
                            total_weight -= weight_to_add
                            total_weight = round(total_weight, 3)

                    self.weights_matrix[source_node][source_node] = total_weight

    def computeInitNodesAndSourcesForATarget(self):
        """
            Method to compute 'init' nodes (an 'init' node is a node which is not a target), in the graph.
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
            source_node : The source node of the edge to compute weight
            target_node : The target node of the edge to compute weight
            local_probability_to_come : The local probability to the event to come
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
