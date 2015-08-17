from libs.graph_generation.graph_generation_algorithms.MuscoGraph import MuscoGraph
from libs.graph_generation.graph_generation_algorithms.BarabasiGraph import BarabasiGraph

from time import sleep

def musco_script():
    """
        Script to create and do some tests on Musco graphs
    """

    musco_graph = MuscoGraph("musco", 25, 37)
    musco_graph.run()

    learning_set_m, testing_set_m = musco_graph.generateExamples()
    learning_set_m.run()

    print("Set : {}\n".format(learning_set_m.tests))

    weights_matrix_m = learning_set_m.makeSomeLearning()

    print("{0}\n".format(weights_matrix_m))

    testing_set_m.run()

    print("Weights matrix: {}".format(testing_set_m.makeSomeTesting(weights_matrix_m)))
    print("Test matrix: {}".format(testing_set_m.tests))

def barabasi_script():
    """
        Script to create and do some tests on Barabasi graphs
    """

    barabasi_graph = BarabasiGraph("musco", 25, 5, 37)
    barabasi_graph.run()

    learning_set_b, testing_set_b = barabasi_graph.generateExamples()
    learning_set_b.run()

    print("Set : {}\n".format(learning_set_b.tests))

    weights_matrix_b = learning_set_b.makeSomeLearning()

    print("{0}\n".format(weights_matrix_b))

    testing_set_b.run()

    print("Weights matrix: {}".format(testing_set_b.makeSomeTesting(weights_matrix_b)))
    print("Test matrix: {}".format(testing_set_b.tests))

if __name__ == "__main__":

    musco_script()
    sleep(5)
    barabasi_script()
