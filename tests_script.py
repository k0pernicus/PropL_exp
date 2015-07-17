from libs.graph_generation.graph_generation_algorithms.MuscoGraph import MuscoGraph
from libs.graph_generation.graph_generation_algorithms.BarabasiGraph import BarabasiGraph

if __name__ == "__main__":

    musco_graph = MuscoGraph("musco", 25, 37)
    musco_graph.run()

    learning_set, testing_set = musco_graph.generateExamples()
    learning_set.run()

    print("Set : {}\n".format(learning_set.tests))

    weights_matrix = learning_set.makeSomeLearning()

    print("{0}\n".format(weights_matrix))

    testing_set.run()

    print("Weights matrix: {}".format(testing_set.makeSomeTesting(weights_matrix)))
    print("Test matrix: {}".format(testing_set.tests))
