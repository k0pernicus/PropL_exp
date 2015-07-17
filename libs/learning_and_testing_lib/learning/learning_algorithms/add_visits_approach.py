import networkx as nx

def getExistingPathsFrom(path):
    """
    Function to transform the list of nodes (all_paths) to a list of tuples (source, target)
    Ex: [node1, node2, node3, node4, ...] -> [(node1, node2),(node2, node3), (node3, node4), (node4,...)]
    path: A path in the usegraph
    """

    return [(path[a], path[a + 1]) for a in range(0, len(path) - 1)]

def add_visits_approach(graph, nb_batch, tests):
    """
    Algorithm to compute the weight of each edge.
    Returns the weights matrix.
    The algorithm is really simple : in the tests list, we pop a source node and the list of his impacted nodes.
    For those, we return the list of available paths between the source node and impacted nodes, and add +1 to their edge (including the edge between the source node and itself).
    graph : A Graph object
    nb_batch : An integer to represent the number of iteration to learn (can accurate or not learning results)
    tests : Tests to learn with
    """

    weights_matrix = {}

    for test in tests:

        source_node = test[0]
        final_nodes = test[1]

        #Initialization of the weights matrix
        if not source_node in weights_matrix:
            weights_matrix[source_node] = {}
            weights_matrix[source_node][source_node] = 1
        else:
            #add +1 to the edge between the source node and itself
            weights_matrix[source_node][source_node] += 1

        #for each final node
        for final_node in final_nodes:
            #get all paths between the source node and the final node
            paths_between_source_and_final_nodes = nx.all_simple_paths(graph.graph, source_node, final_node)

            #for each path
            for path in paths_between_source_and_final_nodes:

                #for each edge
                for edge in getExistingPathsFrom(path):

                    #get the source and the target
                    source_edge = edge[0]
                    target_edge = edge[1]

                    #init the source_edge dict into weights_matrix
                    if not source_edge in weights_matrix:
                        weights_matrix[source_edge] = {}
                        weights_matrix[source_edge][source_edge] = 1

                    #add the weight between the new source node and the target node, while the target is not a final node
                    if not target_edge in weights_matrix[source_edge]:
                        weights_matrix[source_edge][target_edge] = 1
                    else:
                        weights_matrix[source_edge][target_edge] += 1

    return weights_matrix
