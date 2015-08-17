from libs.learning_and_testing_lib.DefaultStructure import DefaultStructure
from libs.learning_and_testing_lib.testing.testing_algorithms.test_each_edge_approach import test_each_edge_approach
from libs.learning_and_testing_lib.testing.testing_algorithms.test_each_path_approach import test_each_path_approach

import os

libs_dir = "libs/"
learning_and_testing_dir = "learning_and_testing_lib/"
testing_dir = "testing/"
testing_algo_dir = "testing_algorithms/"

testing_algorithm_functions = {
    'test_each_edge_approach' : test_each_edge_approach,
    'test_each_path_approach' : test_each_path_approach
}

not_usefull_files = [".DS_Store", "__pycache__", "__pycache__/", "__init__.py"]

class TestingSet(DefaultStructure):
    """
        Object which contains the data set to test learned probabilities (by the learning algorithm).
        id : The id of this object
        graph : The graph which the data set from
        tests : Data set (list of couple source_node : targets_node) to test
        debug_mod : A boolean to know if the graph is on debugging mod or not
    """

    def __init__(self, id, graph, tests, debug_mod):
        super().__init__(id, graph, tests, debug_mod)

    def run(self):
        """
            Method to initialize the testing method approach used.
        """
        self.testing_algorithm = self.setTestingAlgorithm()

    def setTestingAlgorithm(self):
        """
            Method to set the testing algorithm used for this part.
            testing_algorithm : A string which represents the testing algorithm used (for each edge, for each path,...)
        """
        current_dir = os.getcwd()
        if current_dir[-1] != '/':
            current_dir += '/'

        testing_algorithms_available = os.listdir("{0}{1}{2}{3}{4}".format(current_dir, libs_dir, learning_and_testing_dir, testing_dir, testing_algo_dir))

        print("List of testing algorithms:")

        for testing_algorithm in testing_algorithms_available:
            if not testing_algorithm in not_usefull_files:
                print("\t{} : {}".format(testing_algorithms_available.index(testing_algorithm), testing_algorithm.split("_approach")[0]))

        print("\n")

        user_choice = int(input("Your choice [0, 1, ...]: "))

        if not user_choice < len(testing_algorithms_available):
            print("Invalid...")
            sys.exit()

        return testing_algorithms_available[user_choice].split(".py")[0]

    def to_dic(self):

        testing_set_m_dic = {}

        for test_couple in self.tests:
            node_mutated = test_couple[0]

            if not node_mutated in testing_set_m_dic:
                testing_set_m_dic[node_mutated] = []

            for target_impacted in test_couple[1]:
                if not target_impacted in testing_set_m_dic[node_mutated]:
                    testing_set_m_dic[node_mutated].append(target_impacted)

        return testing_set_m_dic

    def makeSomeTesting(self, weights_matrix):
        """
            Method to return results with the weight matrix, given as parameter
        """
        f = testing_algorithm_functions[self.testing_algorithm]

        return f(self.graph, weights_matrix, self.tests)

    def compareResultsWith(self, weights_matrix_computed):
        error_prediction = 0

        good_prediction = 0

        testing_set_m_dic = self.to_dic()

        print("testing set {0}".format(testing_set_m_dic))

        for node_mutated in testing_set_m_dic:
            if (len(testing_set_m_dic[node_mutated]) == 0) and (len(weights_matrix_computed[node_mutated]) == 0):
                print("OK for {0}".format(node_mutated))
                good_prediction += 1
            elif (len(testing_set_m_dic[node_mutated]) == 0) and (len(weights_matrix_computed[node_mutated]) != 0):
                error_prediction += len(weights_matrix_computed[node_mutated])
            elif (len(weights_matrix_computed[node_mutated]) == 0):
                error_prediction += len(testing_set_m_dic[node_mutated])
            else:
                nb_impacted_nodes = 0
                for target_impacted in testing_set_m_dic[node_mutated]:
                    if target_impacted in weights_matrix_computed[node_mutated]:
                        good_prediction += 1
                        nb_impacted_nodes += 1
                    else:
                        error_prediction += 1
                if len(weights_matrix_computed[node_mutated]) != 0:
                    error_prediction += len(weights_matrix_computed[node_mutated]) - nb_impacted_nodes
            print("{0} -> {1} errors / {2} good".format(node_mutated, error_prediction, good_prediction))

        return good_prediction, error_prediction
