def isEmpty(list):
    """
    Abstract: Function to know if the list (as parameter) is empty or not
    """

    return len(list) == 0

def chunksList(list, n):
    """
    Yield successive n-sized chunks from list
    list: The list to chunks
    n: The number of elements in each sublist
    """
    list_to_return = []
    for i in range(0, len(list), n):
        list_to_return += [list[i:i+n]]
    return list_to_return

def getExistingPathsFrom(path):
    """
    Function to transform the list of nodes (all_paths) to a list of tuples (source, target)
    Ex: [node1, node2, node3, node4, ...] -> [(node1, node2),(node2, node3), (node3, node4), (node4,...)]
    path: A path in the usegraph
    """

    return [(path[a], path[a + 1]) for a in range(0, len(path) - 1)]
