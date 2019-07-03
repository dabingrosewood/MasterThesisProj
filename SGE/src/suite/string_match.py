import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from util.cython.interface import edit_dis
from util.math_func import *
import numpy as np
from util.get_data import *

# dataset_path = '../resources/vladislavleva4/'


class String_match():

    def __init__(self, run):
        self.__train_set = []
        self.__test_set = []
        self.__invalid_fitness = np.nan
        self.__run = run
        self.test_set_size = len(self.__test_set)
        self.target="Hello world! I am testing GE."

        # Find number of variables.


    # def evaluate(self,individual):
    #     # print "individual= %s" % (individual)
    #     guess = individual
    #
    #     # fitness=interface.editDistance(self.target,guess)
    #
    #     error = max(len(self.target), len(guess))+0.001
    #     # Loops as long as the shorter of two strings
    #     for (t_p, g_p) in zip(self.target, guess):
    #         if t_p == g_p:
    #             # Perfect match.
    #             error -= 1
    #         else:
    #             # Imperfect match, find ASCII distance to match.
    #             error -= 1.0 / float((1 + (abs(ord(t_p) - ord(g_p)))))
    #     return (error, {})

    def evaluate(self, individual):
        print "individual= %s" %(individual)
        try:
            error = edit_dis(individual, self.target)
        except:

            error=self.__invalid_fitness

        return (error, {})



if __name__ == "__main__":
    import core.grammar as grammar
    import core.sge
    from configs.standard import RUN

    experience_name = "string_match/"
    grammar = grammar.Grammar("../grammars/string_match.bnf", 15)
    evaluation_function = String_match(RUN)
    core.sge.evolutionary_algorithm(grammar=grammar, eval_func=evaluation_function, exp_name=experience_name)