from libs.utils.utils import getExistingPathsFrom

import networkx as nx

import random

def test_each_path_approach(graph, weights_matrix, tests):
    """
        Function to test, on testing examples, the weights matrix.
        Random probability (between 0 and 1) for each path.
        graph : The graph to compute tests with weights_matrix
        weights_matrix : The weights matrix of usefull edges in the graph
        tests : Tests made by a learning algorithm (see Learning object)
    """

    results = {}

    for test in tests:

        source_node = test[0]

        results[source_node] = []

        for final_node in graph.final_nodes_for_source_node[source_node]:

            random_prop = random.uniform(0,1)

            prob_path = 1

            paths_between_source_node_and_final_nodes = nx.all_simple_paths(graph.graph, source_node, final_node)

            for path in paths_between_source_node_and_final_nodes:

                for edge in getExistingPathsFrom(path):

                    source_edge = edge[0]
                    target_edge = edge[1]

                    try:
                        prob_path = prob_path * (weights_matrix[source_edge][target_edge] / weights_matrix[source_edge][source_edge])
                    except Exception as e:
                        prob_path = 0

                if random_prop <= prob_path:
                    results[source_node].append(final_node)

        results[source_node] = list(set(results[source_node]))

    return results
