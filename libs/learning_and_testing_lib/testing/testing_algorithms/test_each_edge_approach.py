from libs.utils.utils import getExistingPathsFrom

import networkx as nx

import random

def test_each_edge_approach(graph, weights_matrix, tests):
    """
        Function to test, on testing examples, the weights matrix.
        Random probability (between 0 and 1) for each edge.
        graph : The graph to compute tests with weights_matrix
        weights_matrix : The weights matrix of usefull edges in the graph
        tests : Tests made by a learning algorithm (see Learning object)
    """

    results = {}

    for test in tests:

        source_node = test[0]

        results[source_node] = []

        for final_node in graph.final_nodes_for_source_node[source_node]:

            prob_path = 1

            paths_between_source_node_and_final_nodes = nx.all_simple_paths(graph.graph, source_node, final_node)

            for path in paths_between_source_node_and_final_nodes:

                find = True

                for edge in getExistingPathsFrom(path):

                    random_prop = random.uniform(0,1)

                    source_edge = edge[0]
                    target_edge = edge[1]

                    try:
                        proportion_of_the_target_for_the_source = (weights_matrix[source_edge][target_edge] / weights_matrix[source_edge][source_edge])
                        if (proportion_of_the_target_for_the_source < 0) or (proportion_of_the_target_for_the_source > 1):
                            print("ERROR : proportion_of_the_target_for_the_source is not ok ({0} for source {1} and target {2})".format(proportion_of_the_target_for_the_source, weights_matrix[source_edge][source_edge], weights_matrix[source_edge][target_edge]))
                        if random_prop > proportion_of_the_target_for_the_source:
                            find = False
                    except Exception as e:
                        find = False

                if find:
                    results[source_node].append(final_node)

        results[source_node] = list(set(results[source_node]))

    return results
