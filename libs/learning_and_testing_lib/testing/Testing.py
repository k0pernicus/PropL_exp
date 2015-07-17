from libs.learning_and_testing_lib.DefaultStructure import DefaultStructure

class TestingSet(DefaultStructure):

    def __init__(self, id, graph, tests, debug_mod):
        super().__init__(id, graph, tests, debug_mod)
