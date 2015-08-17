from libs.learning_and_testing_lib.DefaultStructure import DefaultStructure

from libs.learning_and_testing_lib.learning.learning_algorithms.add_visits_approach import add_visits_approach
# from libs.learning_and_testing_lib.learning.learning_algorithms.min_and_max_approach import min_and_max_approach
# from libs.learning_and_testing_lib.learning.learning_algorithms.tag_each_usefull_edge_approach import tag_each_usefull_edge_approach
# from libs.learning_and_testing_lib.learning.learning_algorithms.update_each_path_approach import update_each_path_approach

import os

libs_dir = "libs/"
learning_and_testing_dir = "learning_and_testing_lib/"
learning_dir = "learning/"
learning_algo_dir = "learning_algorithms/"

learning_algorithm_functions = {
    'add_visits_approach' : add_visits_approach,
    #'min_and_max_approach' : min_and_max_approach,
    #'tag_each_usefull_edge_approach' : tag_each_usefull_edge_approach,
    #'update_each_path_approach' : update_each_path_approach
}

not_usefull_files = [".DS_Store", "__pycache__", "__pycache__/", "__init__.py"]

class LearningSet(DefaultStructure):
    """
        Object which contains the data set to learn the probability of each usefull edge.
        id : The id of this object
        graph : The graph which the data set from
        tests : Data set (list of couple source_node : targets_node) to learn
        debug_mod : A boolean to know if the graph is on debugging mod or not
    """

    def __init__(self, id, graph, tests, debug_mod):
        super().__init__(id, graph, tests, debug_mod)
        self.batch_nbr = 1
        self.learning_algorithm = ""

    def run(self):
        """
            Method to initialize the learning method approach used.
        """
        self.learning_algorithm = self.setLearningAlgorithm()

    def setLearningAlgorithm(self):
        """
            Method to set the learning algorithm used for this part.
            learning_algorithm : A string which represents the learning algorithm used (dichotomic, min_and_max, tag_each_usefull_edge,...)
        """
        current_dir = os.getcwd()
        if current_dir[-1] != '/':
            current_dir += '/'

        learning_algorithms_available = os.listdir("{0}{1}{2}{3}{4}".format(current_dir, libs_dir, learning_and_testing_dir, learning_dir, learning_algo_dir))

        print("List of learning algorithms:")

        for learning_algorithm in learning_algorithms_available:
            if (not learning_algorithm in not_usefull_files) and (learning_algorithm.split(".py")[0] in learning_algorithm_functions):
                print("\t{} : {}".format(learning_algorithms_available.index(learning_algorithm), learning_algorithm.split("_approach")[0]))

        print("\n")

        user_choice = int(input("Your choice [0, 1, ...]: "))

        if not user_choice < len(learning_algorithms_available):
            print("Invalid...")
            sys.exit()

        return learning_algorithms_available[user_choice].split(".py")[0]

    def makeSomeLearning(self):
        """
            Method to return the weights matrix, computed by the learning algorithm function choosen
        """
        f = learning_algorithm_functions[self.learning_algorithm]

        return f(self.graph, self.batch_nbr, self.tests)
