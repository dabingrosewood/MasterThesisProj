import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from util.cython.interface import fitness_rmse
from util.math_func import *
import numpy as np
from util.get_data import *

# dataset_path = '../resources/vladislavleva4/'


class Supervised_learning():

    def __init__(self, run):
        self.__train_set = []
        self.__test_set = []
        self.__invalid_fitness = np.nan
        self.__run = run
        self.test_set_size = len(self.__test_set)
        self.training_in, self.training_exp, self.test_in, self.test_exp = \
            get_data('vladislavleva4/Train.txt', 'vladislavleva4/Test.txt')

        # Find number of variables.
        self.n_vars = np.shape(self.training_in)[0]



    def evaluate(self, individual):
        # print "individual= %s" %(individual)

        if individual == None:
            return None

        x = self.training_in
        y = self.training_exp


        try:
            yhat = eval(individual)
        except (OverflowError, ValueError,FloatingPointError) as e:
            yhat=self.__invalid_fitness
        if type(yhat) in [float, np.float64]:
            # this is the situation that the phenotype is one float.
            # Then to build an array

            # print("ind.phenotype==",ind.phenotype)
            yhat = np.full(np.shape(y), yhat, dtype=float)

        elif yhat.size == 1:
            # for the problem that yhat is ndarray but size is 1
            yhat = np.full(np.shape(y), yhat, dtype=float)

        y = y.copy(order='C')
        yhat = yhat.copy(order='C')

        error = fitness_rmse(y, yhat)
        # print(y,yhat)
        # print 'error=%f' %error

        x = self.test_in
        y = self.test_exp

        try:
            yhat = eval(individual)
        except (OverflowError, ValueError,FloatingPointError) as e:
            yhat=self.__invalid_fitness

        if type(yhat) in [float, np.float64]:
            # this is the situation that the phenotype is one float.
            # Then to build an array

            # print("ind.phenotype==",ind.phenotype)
            yhat = np.full(np.shape(y), yhat, dtype=float)

        elif yhat.size == 1:
            # for the problem that yhat is ndarray but size is 1
            yhat = np.full(np.shape(y), yhat, dtype=float)

        y = y.copy(order='C')
        yhat = yhat.copy(order='C')

        test_error = fitness_rmse(y,yhat)

        return (error, {'generation': 0, "evals": 1, "test_error": test_error})

    def __str__(self):
        descr = "len(train):%d len(test):%d\n\n" % (len(self.__train_set), len(self.__test_set))
        descr += "Training_set:\n"
        for i in self.__train_set[0:5]: descr += str(i) + "\n"
        descr += "Test_set:\n"
        for i in self.__test_set[0:5]: descr += str(i) + "\n"
        return descr


if __name__ == "__main__":
    import core.grammar as grammar
    import core.sge
    from configs.standard import RUN

    experience_name = "Supervised_learning_test/"
    grammar = grammar.Grammar("../grammars/vladislavleva4.bnf", 5)
    evaluation_function = Supervised_learning(RUN)
    core.sge.evolutionary_algorithm(grammar=grammar, eval_func=evaluation_function, exp_name=experience_name)