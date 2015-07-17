class DefaultStructure(object):
    """
        Default structure of the object to get testing and learning data set.
        id : The id of the data set.
        graph : The graph which is the origin of the data set
        tests : Array of tests - a test is represents by a dictionary {"source" : node_source, "targets" : [node_target1, node_target2, ...]}
        debug_mod : A boolean to know if the graph is on debugging mod or not
    """

    def __init__(self, id, graph, tests, debug_mod):
        self.id = id
        self.graph = graph
        self.tests = tests
        self.debug_mod = debug_mod

    def __del__(self):
        print("The structure {} has been deleted.".format(self.id))

    def printTests(self):
        """
            Usefull method to print out correctly tests for this structure.
        """
        for test in self.tests:
            print("Source id : {}".format(test["source"]))
            for target_node in test["targets"]:
                print("\tTarget id : {}".format(target_node))
